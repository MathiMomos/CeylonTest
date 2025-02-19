from CeylonInterpreter.NodeVisitor.NodeVisitor import NodeVisitor
from CeylonInterpreter.CallStack.CallStack import CallStack
from CeylonInterpreter.AR.AR import AR, ART
from CeylonInterpreter.AR.Member import Member, Number_type, String_type, Boolean_type, Null_type
from CeylonInterpreter.Tokens.TokenType import TokenType
from AST.Special import NoOp
from AST.Function import Return
from AST.Flow import If

class Interpreter(NodeVisitor):

    def __init__(self):
        self.call_stack = CallStack()

# PROGRAM

    def visit_Program(self, node):
        program_ar = AR(
            name="PROGRAM",
            ar_type=ART.PROGRAM,
            nesting_level=1,
            enclosing_ar=None
        )

        self.call_stack.push(program_ar) # adds the execution of the program to the CALL_STACK
        self.visit(node.block_node) # visits the program's body

        print(self.call_stack.peek())

        self.call_stack.pop() # end with the program

# ESTRUCTURES

    def visit_FunctionStmt(self, node):
        pass

    def visit_If(self, node):

        condition_check = False

        if isinstance(node.condition, NoOp):
            condition_check = True # initial
        else:
            condition_check, _ = self.visit(node.condition) # gets the truth value

        if not condition_check: # if the condition is not true
            self.visit(node.right) # elif or else
            return

        # condition true, executes the block

        if_ar = AR(
            name="IF",
            ar_type=ART.IF,
            nesting_level=self.call_stack.peek().nesting_level+1,
            enclosing_ar=self.call_stack.peek()
        )

        self.call_stack.push(if_ar)
        node_result = self.visit(node.left) # executes the block

        if isinstance(node_result, Return):
            print(self.call_stack.pop())
            return node_result

        print(self.call_stack.peek())

        self.call_stack.pop()


    def visit_While(self, node):
        condition_check, _ = self.visit(node.condition)

        if not condition_check:
            return

        # current_ar = self.call_stack.peek()

        while_ar = AR(
            name="WHILE",
            ar_type=ART.WHILE,
            nesting_level=self.call_stack.peek().nesting_level+1,
            enclosing_ar=self.call_stack.peek()
        )

        self.call_stack.push(while_ar)

        node_result = self.visit(node.child)

        if isinstance(node_result, Return):
            print(self.call_stack.pop())
            return node_result

        self.visit(node)

        print(self.call_stack.peek())

        self.call_stack.pop()

    def visit_For(self, node):
        ar_for = AR(
            name="FOR",
            ar_type=ART.FOR,
            nesting_level=self.call_stack.peek().nesting_level+1,
            enclosing_ar=self.call_stack.peek()
        )

        self.call_stack.push(ar_for)
        self.visit(node.init_var)

        while True:
            condition_check, _ = self.visit(node.condition)

            if not condition_check:
                print(self.call_stack.peek())
                self.call_stack.pop()
                return

            node_result = self.visit(node.block_node)

            if isinstance(node_result, Return):
                print(self.call_stack.pop())
                return node_result

            self.visit(node.auto)


    def visit_Block(self, node):
        for statement in node.statement_list:
            self.visit(statement)

    def visit_ScopedBlock(self, node):
        for statement in node.statement_list:
            if isinstance(statement, Return):
                return statement # Node Return
            node_ = self.visit(statement)

            if isinstance(node_, Return):
                return node_

# PARAMETERS AND ARGUMENTS

    def visit_Parameter(self, node):
        pass

    def visit_FunctionCall(self, node):
        func_symbol = node.func_symbol

        if isinstance(node.child, NoOp):
            arguments = []
        else:
            arguments = self.visit(node.child)

        func_call_ar = AR(
            name="FUNC_CALL " + node.func_name,
            ar_type=ART.FUNCTION,
            nesting_level=self.call_stack.peek().nesting_level+1,
            enclosing_ar=self.call_stack.peek()
        )

        # Detects a runtime error, the number of arguments must to be the same of the number of formal parameters

        if len(arguments) != len(func_symbol.params):
            raise Exception("the number of arguments must to be the same of the number of formal parameters in the function call %s" % func_symbol.name)

        # Arguments processing
        for parameter, argument in zip(func_symbol.params, arguments):
            member = Member(
                name=parameter.name,
                value=argument[0],
                member_type=argument[1]
            )

            member.var_type = "Var"
            func_call_ar[member.name] = member

        self.call_stack.push(func_call_ar)

        return_node = self.visit(func_symbol.scoped_block_node)
        # func_call_ar.returning_value = returning_value

        if isinstance(return_node, Return):
            returning_value = self.visit(return_node)
        else:
            returning_value = ("null", Null_type)

        print(self.call_stack.pop())

        return returning_value

    def visit_Argument(self, node):
        arguments = []
        value, type_ = self.visit(node.left)
        tuple_arg = (value, type_)
        arguments.append(tuple_arg)

        if isinstance(node.right, NoOp):
            return arguments

        arguments.extend(self.visit(node.right))

        return arguments

    def visit_Return(self, node):
        return self.visit(node.child)
        # later

# PRINT

    def visit_Print(self, node):
        value, type_ = self.visit(node.child)
        print(value)

# VARIABLES AND CONSTANTS

    def visit_Var(self, node):
        var_name = node.var_name
        current_ar = self.call_stack.peek()
        var_member = current_ar.get(var_name)

        if var_member is None:
            raise Exception(f"Variable {var_name} not found.")

        value = var_member.value
        type_ = var_member.member_type
        return value, type_

    def visit_VarAssign(self, node):
        var_name = node.left.var_name
        current_ar = self.call_stack.peek()
        var_member = current_ar.get(var_name)

        new_var_value, new_var_type = self.visit(node.right)

        if var_member is None:
            new_member = Member(
                name=var_name,
                value=new_var_value,
                member_type=new_var_type,
            )

            new_member.var_type = "Var"

            current_ar.set(new_member.name, new_member)
            return

        if var_member.var_type == "Final":
            raise Exception(f"Final {var_name} cannot be reassigned.")

        new_var_value, new_var_type = self.visit(node.right)

        var_member.value = new_var_value
        var_member.member_type = new_var_type

    def visit_FinalAssign(self, node):
        final_name = node.left.var_name
        current_ar = self.call_stack.peek()
        final_member = current_ar.get(final_name)

        final_value, final_type = self.visit(node.right)

        if final_member is None:
            new_member = Member(
                name=final_name,
                value=final_value,
                member_type=final_type,
            )

            new_member.var_type = "Final"

            current_ar.set(new_member.name, new_member)
            return

        if final_member.var_type == "Var":
            raise Exception(f"Variable {final_name} already exists.")

        raise Exception(f"Final {final_name} cannot be reassigned.")

    def visit_VarAuto(self, node):
        _, type_ = self.visit(node.child)

        var_name = node.child.var_name
        current_ar = self.call_stack.peek()
        var_member = current_ar.get(var_name)

        if type_.name != Number_type.name:
            raise Exception(f"Type {type_.name} is not number. Self operations is not allowed.")

        op = node.op.value

        if op == TokenType.INCREMENT.value:
            var_member.value += 1
        elif op == TokenType.DECREMENT.value:
            var_member.value -=1

    def visit_VarCompoundAssign(self, node):
        _, type_ = self.visit(node.child)

        var_name = node.left.var_name
        current_ar = self.call_stack.peek()
        var_member = current_ar.get(var_name)

        if type_ != Number_type.name:
            raise Exception(f"Type {type_} is not number. Self operations is not allowed.")

        if var_member.var_type == "Final":
            raise Exception(f"Final {var_name} cannot be reassigned.")

        op = node.op.value

        value, _ = self.visit(node.right)

        if op == TokenType.PLUS_ASSIGN:
            var_member.value += value
        elif op == TokenType.MINUS_ASSIGN:
            var_member.value -= value
        elif op == TokenType.TIMES_ASSIGN:
            var_member.value *= value
        elif op == TokenType.DIVIDE_ASSIGN:
            var_member.value /= value
        elif op == TokenType.POWER_ASSIGN:
            var_member.value **= value
        elif op == TokenType.MODULO_ASSIGN:
            var_member.value %= value
        elif op == TokenType.INT_DIVIDE_ASSIGN:
            var_member.value //= value

# OPERATIONS

    def visit_BinOp(self, node):
        left_value, left_type = self.visit(node.left)
        right_value, right_type = self.visit(node.right)

        type_ = Number_type
        type_name = type_.name

        op = node.op.value

        if left_type.name != type_name:
            raise Exception("Type %s is not compatible with binary arithmetic operation." % type_name)

        if right_type.name != type_name:
            raise Exception("Type %s is not compatible with binary arithmetic operation." % type_name)

        value = 0

        if op == TokenType.PLUS.value:
            value = left_value + right_value
        elif op == TokenType.MINUS.value:
            value = left_value - right_value
        elif op == TokenType.TIMES.value:
            value = left_value * right_value
        elif op == TokenType.DIVIDE.value:
            if right_value == 0:
                raise Exception("Zero division error")
            value = left_value / right_value
        elif op == TokenType.POWER.value:
            value = left_value ** right_value
        elif op == TokenType.MODULO.value:
            value = left_value % right_value
        elif op == TokenType.INT_DIVIDE.value:
            if right_value == 0:
                raise Exception("Zero division error")
            value = left_value // right_value

        return value, type_

    def visit_StringConcat(self, node):
        left_value, left_type = self.visit(node.left)
        right_value, right_type = self.visit(node.right)

        type_ = String_type
        type_name = type_.name

        if left_type.name != type_name:
            raise Exception("Type %s is not compatible with string concatenation." % type_name)

        if right_type.name != type_name:
            raise Exception("Type %s is not compatible with string concatenation." % type_name)

        value = left_value + right_value

        return value, type_

    def visit_BinBooleanOp(self, node):
        left_value, left_type = self.visit(node.left)
        right_value, right_type = self.visit(node.right)

        type_ = Boolean_type
        type_name = type_.name

        op = node.op.value

        if left_type.name != type_name:
            raise Exception("Type %s is not compatible with binary boolean operation." % type_name)

        if right_type.name != type_name:
            raise Exception("Type %s is not compatible with binary boolean operation." % type_name)

        value = False

        if op == TokenType.AND.value:
            value = left_value & right_value
        elif op == TokenType.OR.value:
            value = left_value | right_value

        return value, type_

    def visit_BinComp(self, node):
        left_value, left_type = self.visit(node.left)
        right_value, right_type = self.visit(node.right)

        type_ = Boolean_type
        # type_name = type_.name

        value = False

        op = node.op.value

        if op == TokenType.EQ.value:
            value = left_value == right_value
        elif op == TokenType.NE.value:
            value = left_value != right_value
        elif op == TokenType.LT.value:
            value = left_value < right_value
        elif op == TokenType.GT.value:
            value = left_value > right_value
        elif op == TokenType.LE.value:
            value = left_value <= right_value
        elif op == TokenType.GE.value:
            value = left_value >= right_value

        return value, type_

    # return value, type_

    def visit_Unary(self, node):
        op = node.op.value
        value, type_ = self.visit(node.child)

        if type_.name != Number_type.name:
            raise Exception("Type %s is not compatible with unary arithmetic operation." % type_.name)

        if op == TokenType.PLUS.value:
            return +value, type_
        return -value, type_


    def visit_UnaryBoolean(self, node):
        value, type_ = self.visit(node.child)

        if type_.name != Boolean_type.name:
            raise Exception("Type %s is not compatible with unary boolean operation." % type_.name)

        return not value, type_

    def visit_Ternary(self, node):
        value, _ = self.visit(node.condition)

        if value:
            left_value, left_type = self.visit(node.left)
            return left_value, left_type
        else:
            right_value, right_type = self.visit(node.right)
            return right_value, right_type

# IMMUTABLE TERMINALS

    def visit_String(self, node): # returns a tuple (value, type)
        value = node.value
        type_ = node.type
        return value, type_

    def visit_Num(self, node): # returns a tuple (value, type)
        value = node.value
        type_ = node.type
        return value, type_

    def visit_Boolean(self, node): # returns a tuple (value, type)
        value = node.value
        type_ = node.type
        return value, type_

    def visit_Null(self, node): # returns a tuple (value, type)
        value = node.value
        type_ = node.type
        return value, type_

# NOOP HANDLING

    def visit_NoOp(self, node):
        pass