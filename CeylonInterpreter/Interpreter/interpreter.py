from CeylonInterpreter.NodeVisitor.NodeVisitor import NodeVisitor
from CeylonInterpreter.CallStack.CallStack import CallStack
from CeylonInterpreter.AR.AR import AR, ART
from CeylonInterpreter.AR.Member import Member, Number_type, String_type, Boolean_type, Null_type
from CeylonInterpreter.Tokens.TokenType import TokenType
from AST.Special import NoOp
from AST.Function import Return

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

        self.call_stack.pop() # end with the program

    def visit_FunctionStmt(self, node):
        pass

# STRUCTURES

    def visit_Switch(self, node):
        result_ = self.visit(node.right)
        return result_

    def visit_Case(self, node):
        check_condition, _ = self.visit(node.comp)

        if not check_condition:
            result_ = self.visit(node.case)
            return result_

        case_ar = AR(
            name="CASE",
            ar_type=ART.CASE,
            nesting_level=self.call_stack.peek().nesting_level + 1,
            enclosing_ar=self.call_stack.peek()
        )

        # Adds the AR to the call_stack
        self.call_stack.push(case_ar)

        result_ = self.visit(node.block)

        if result_:
            self.call_stack.pop()
            return result_

        self.call_stack.pop()


    def visit_If(self, node):

        # Checking if the condition is true or false

        # Checks if the actual structure is else
        if isinstance(node.condition, NoOp):
            condition_check = True # initial

        # The actual structure is if or elif, checks the condition visiting the BinBooleanOp node
        else:
            condition_check, _ = self.visit(node.condition) # gets the truth value

        # If the condition of the actual conditional structure is false, then visits the next
        # and returns the return node (if exists)
        if not condition_check: # if the condition is not true
            return_ = self.visit(node.right) # Maybe return a tuple with the results of the return statement
            return return_ # return_ can be None, no problem

        # The actual if, elif or else has the condition true

        # Creates the corresponding AR of the IF
        if_ar = AR(
            name="IF",
            ar_type=ART.IF,
            nesting_level=self.call_stack.peek().nesting_level+1,
            enclosing_ar=self.call_stack.peek()
        )

        # Adds the AR to the call_stack
        self.call_stack.push(if_ar)

        # Executes the block or scoped block
        result_ = self.visit(node.left) # If returning something, must be a tuple with the data result of the Return node evaluated

        if result_:
            self.call_stack.pop()
            return result_

        self.call_stack.pop()


    def visit_While(self, node):
        # Gets the resolution of the condition (true or false)
        condition_check, _ = self.visit(node.condition)

        # If the condition is false, then the While loop is ignored (this is the first checking)
        if not condition_check:
            return

        # Creates the AR for the While loop
        while_ar = AR(
            name="WHILE",
            ar_type=ART.WHILE,
            nesting_level=self.call_stack.peek().nesting_level+1,
            enclosing_ar=self.call_stack.peek()
        )

        # Push the While AR to the call stack
        self.call_stack.push(while_ar)

        # result_ is the possibly result of a Return execution inside the While loop. Can be None or a tuple with
        # the data
        result_ = self.visit(node.child) # visits the scoped block because the condition check still true

        # Checks if the result is not none
        if result_:
            self.call_stack.pop() # Pops the While AR
            return result_ # returns the tuple of the return data

        result_ = self.visit(node) # visits the While node again, the While is recursive this is the reason for the double evaluation of the result_

        # Checks if the result is not none
        if result_:
            self.call_stack.pop()  # Pops the While AR
            return result_ # returns the tuple of the return data

        self.call_stack.pop() # Pops and implicitly returns None

    def visit_For(self, node):
        # Creates the For AR because it needs to init the var inside
        ar_for = AR(
            name="FOR",
            ar_type=ART.FOR,
            nesting_level=self.call_stack.peek().nesting_level+1,
            enclosing_ar=self.call_stack.peek()
        )

        # Adds the For AR to the call stack
        self.call_stack.push(ar_for)

        # Creates the init var for the For AR
        self.visit(node.init_var)

        # Executes the condition check, the block execution and the auto operation until the condition check makes false
        while True:
            condition_check, _ = self.visit(node.condition) # Executes the condition check

            # Checking the condition

            # Is the condition is false
            if not condition_check:
                self.call_stack.pop() # Stops the For loop
                return # Ends the function and return None

            result_ = self.visit(node.block_node) # In the scoped_block node can exist a Return node

            # If the result is not None
            if result_:
                self.call_stack.pop() # Stops the For loop
                return result_ # Return the data of the internal Return

            self.visit(node.auto) # Do the auto operation


    def visit_Block(self, node):
        # No return statement available, very simple statement_list traversal
        for statement in node.statement_list:
            self.visit(statement)

    def visit_ScopedBlock(self, node):
        for statement in node.statement_list:

            # if the actual statement in the statement_list traversal is a Return, stops all
            if isinstance(statement, Return):
                # runs the Return node in the actual call stack
                return self.visit(statement)

            # result_ is the possibly result of a Return node evaluation
            result_ = self.visit(statement) # The statement can be an If, While or For structure

            # checks if the result is not None (has something to return), if not
            # continues with the statement_list traversal
            if result_:
                return result_

# PARAMETERS AND ARGUMENTS

    def visit_Parameter(self, node):
        pass

    def visit_FunctionCall(self, node):

        # Gets the func_symbol at the FunctionCall node (Assigned in the semantic analysis)
        func_symbol = node.func_symbol

        # Getting the arguments

        # Is the child of the node is an instance of NoOp, then the function call has no arguments
        if isinstance(node.child, NoOp):
            arguments = []

        # The only possibility here is that node.child has an instance of Argument, then visits that node
        else:
            arguments = self.visit(node.child)

        # Creates the AR of the function call
        func_call_ar = AR(
            name="FUNC_CALL " + node.func_name,
            ar_type=ART.FUNCTION,
            nesting_level=self.call_stack.peek().nesting_level+1,
            enclosing_ar=self.call_stack.peek()
        )

        # Detects a runtime error, the number of arguments must be the same of the number of formal parameters
        if len(arguments) != len(func_symbol.params):
            raise Exception("the number of arguments must to be the same of the number of formal parameters in the function call %s" % func_symbol.name)

        # Arguments processing by zipping with the formal parameters of the function
        for parameter, argument in zip(func_symbol.params, arguments):
            member = Member(
                name=parameter.name,
                value=argument[0],
                member_type=argument[1]
            )

            member.var_type = "Var"
            func_call_ar[member.name] = member

        # Pushing the function_call AR to the call stack
        self.call_stack.push(func_call_ar)

        # While visiting the ScopedBlock of the function symbol, expects or not a result (Return evaluation) from inside
        result_ = self.visit(func_symbol.scoped_block_node) # if no return statement, then result_ will be None

        if result_:
            returning_value = result_ # don't worry, is a tuple in the same way below
        else:
            returning_value = ("null", Null_type) # the function doesn't return anything, this is the default value

        self.call_stack.pop()

        return returning_value # returning the tuple, this is it because the function call is an expression too

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
        value, type_ = self.visit(node.child)

        return value, type_
        # later

# SPECIAL (I/O AND CASTING)

    def visit_Print(self, node):
        value, type_ = self.visit(node.child)
        print(value)

    def visit_Scan(self, node):
        var_name = node.child.var_name
        current_ar = self.call_stack.peek()
        var_member = current_ar.get(var_name)

        if var_member is None:
            var_member = Member(
                name=var_name,
                value=None,
                member_type=String_type,
            )
            var_member.var_type = "Var"
            current_ar.set(var_name, var_member)

        if var_member.var_type == "Final":
            raise Exception(f"Final {var_name} cannot be reassigned.")

        var_member.value = input()
        var_member.member_type = String_type

        return var_member.value, var_member.member_type

    def visit_ToStr(self, node):
        value, type_ = self.visit(node.child)

        if type_ != Number_type:
            raise Exception(f"Cannot convert type {type_.name} to a string.")

        value = str(value)
        type_ = String_type

        return value, type_

    def visit_ToNum(self, node):
        value, type_ = self.visit(node.child)

        if type_ != String_type:
            raise Exception(f"Cannot convert type {type_.name} to a number.")

        try:
            value = int(value)
            type_ = Number_type
        except ValueError:
            raise Exception(f"Cannot convert value to a number.")

        return value, type_



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
        _, type_ = self.visit(node.left)

        var_name = node.left.var_name
        current_ar = self.call_stack.peek()
        var_member = current_ar.get(var_name)

        if type_.name != Number_type.name:
            raise Exception(f"Type {type_} is not number. Self operations is not allowed.")

        if var_member.var_type == "Final":
            raise Exception(f"Final {var_name} cannot be reassigned.")

        op = node.op.value

        value, _ = self.visit(node.right)

        if op == TokenType.PLUS_ASSIGN.value:
            var_member.value += value
        elif op == TokenType.MINUS_ASSIGN.value:
            var_member.value -= value
        elif op == TokenType.TIMES_ASSIGN.value:
            var_member.value *= value
        elif op == TokenType.DIVIDE_ASSIGN.value:
            var_member.value /= value
        elif op == TokenType.POWER_ASSIGN.value:
            var_member.value **= value
        elif op == TokenType.MODULO_ASSIGN.value:
            var_member.value %= value
        elif op == TokenType.INT_DIVIDE_ASSIGN.value:
            var_member.value //= value

    def visit_ConcatAssign(self, node):
        _, left_type = self.visit(node.left)
        right_value, _ = self.visit(node.right)

        var_name = node.left.var_name
        current_ar = self.call_stack.peek()
        var_member = current_ar.get(var_name)

        type_ = String_type
        type_name = type_.name

        if left_type.name != type_name:
            raise Exception(f"Type {type_} is not string. Self operations is not allowed.")

        if var_member.var_type == "Final":
            raise Exception(f"Final {var_name} cannot be reassigned.")

        var_member.value += right_value

# OPERATIONS

    def visit_BinOp(self, node):
        left_value, left_type = self.visit(node.left)
        right_value, right_type = self.visit(node.right)

        type_ = Number_type
        type_name = type_.name

        op = node.op.value

        if left_type.name != type_name:
            raise Exception("Type %s is not compatible with binary arithmetic operation." % left_type.name)

        if right_type.name != type_name:
            raise Exception("Type %s is not compatible with binary arithmetic operation." % right_type.name)

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
            raise Exception("Type %s is not compatible with string concatenation." % left_type.name)

        if right_type.name != type_name:
            raise Exception("Type %s is not compatible with string concatenation." % right_type.name)

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