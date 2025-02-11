from TokenType import Token

class AST():
    pass

class ExprNode(AST):
    pass

class BinOp(ExprNode):
    def __init__(self, left: AST, op: Token, right: AST):
        self.left = left
        self.op = op
        self.right = right

class Num(ExprNode):
    def __init__(self, value):
        self.value = value

class Unary(ExprNode):
    def __init__(self, op: Token, child: AST):
        self.op = op
        self.child = child

class String(ExprNode):
    def __init__(self, value, child=None):
        self.value = value
        self.child = child  # String

class BinBooleanOp(ExprNode):
    def __init__(self, left: AST, op: Token, right: AST):
        self.left = left
        self.op = op
        self.right = right

class UnaryBoolean(ExprNode):
    def __init__(self, op, child):
        self.op = op
        self.child = child

class Boolean(ExprNode):
    def __init__(self, value):
        self.value = value

class BinComp(ExprNode):
    def __init__(self, left: ExprNode, op: Token, right: ExprNode):
        self.left = left
        self.op = op
        self.right = right

class Ternary(ExprNode):
    def __init__(self,left : ExprNode, condition : BinBooleanOp, right : ExprNode):
        self.left = left # true expr
        self.condition = condition
        self.right = right # false expr

class Null(ExprNode):
    def __init__(self, value):
        self.value = value

class ScopedBlock(AST):
    def __init__(self, block_name, statement_list):
        self.block_name = block_name
        self.statement_list = statement_list

class Block(AST):
    def __init__(self, block_name, statement_list):
        self.block_name = block_name
        self.statement_list = statement_list

class If(AST):
    def __init__(self, left : Block, condition : BinBooleanOp = None, right = None):
        self.left = left
        self.condition = condition
        self.right = right

class While(AST):
    def __init__(self, condition : BinBooleanOp, child : Block):
        self.condition = condition
        self.child = child

class VarNode(AST):
    pass

class Var(VarNode):
    def __init__(self, var_name):
        self.var_name = var_name

class VarAssign(VarNode):
    def __init__(self, left: Var, right: ExprNode):
        self.left = left
        self.right = right

class VarAuto(VarNode):
    def __init__(self, op: Token, child: Var):
        self.op = op
        self.child = child

class For(AST):
    def __init__(self, init_var : VarAssign, condition : BinBooleanOp, auto : VarAuto, block_node : Block):
        self.init_var = init_var
        self.condition = condition
        self.auto = auto
        self.block_node = block_node

class FinalAssign(VarNode):
    def __init__(self, left: Var, right: ExprNode):
        self.left = left
        self.right = right

class VarCompoundAssign(VarNode):
    def __init__(self, left: Var, op: Token, right: ExprNode):
        self.left = left
        self.op = op
        self.right = right

class FunctionNode(AST):
    pass

class Parameter(FunctionNode):
    def __init__(self, left : Var, right):
        self.left = left
        self.right = right # Parameter

class Argument(FunctionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right # Argument

class FunctionStmt(FunctionNode):
    def __init__(self, func_name, right : ScopedBlock, left : Parameter = None):
        self.left = left
        self.func_name = func_name
        self.right = right

class FunctionCall(FunctionNode):
    def __init__(self, func_name, child : Argument):
        self.func_name = func_name
        self.child = child

class Return():
    def __init__(self, child : ExprNode):
        self.child = child

class NoOp():
    pass

class ASTPrinter:
    def __init__(self, indent=0):
        self.indent = indent

    def print_node(self, node):
        if isinstance(node, BinOp):
            self.print_binop(node)
        elif isinstance(node, Num):
            self.print_num(node)
        elif isinstance(node, Unary):
            self.print_unary(node)
        elif isinstance(node, String):
            self.print_string(node)
        elif isinstance(node, BinBooleanOp):
            self.print_binbooleanop(node)
        elif isinstance(node, UnaryBoolean):
            self.print_unaryboolean(node)
        elif isinstance(node, Boolean):
            self.print_boolean(node)
        elif isinstance(node, Null):
            self.print_null(node)
        elif isinstance(node, ScopedBlock):
            self.print_scopedblock(node)
        elif isinstance(node, Block):
            self.print_block(node)
        elif isinstance(node, If):
            self.print_if(node)
        elif isinstance(node, While):
            self.print_while(node)
        elif isinstance(node, Var):
            self.print_var(node)
        elif isinstance(node, VarAssign):
            self.print_varassign(node)
        elif isinstance(node, FinalAssign):
            self.print_finalassign(node)
        elif isinstance(node, VarCompoundAssign):
            self.print_varcompoundassign(node)
        elif isinstance(node, VarAuto):
            self.print_varauto(node)
        elif isinstance(node, Parameter):
            self.print_parameter(node)
        elif isinstance(node, Argument):
            self.print_argument(node)
        elif isinstance(node, FunctionStmt):
            self.print_functionstmt(node)
        elif isinstance(node, FunctionCall):
            self.print_functioncall(node)
        elif isinstance(node, BinComp):
            self.print_bincomp(node)
        elif isinstance(node, Ternary):
            self.print_ternary(node)
        elif isinstance(node, For):
            self.print_for(node)
        elif isinstance(node, Return):
            self.print_return(node)
        elif isinstance(node, NoOp):
            self.print_noop()
        else:
            print("  " * self.indent + "Unknown node type")

    def print_binop(self, node):
        print("  " * self.indent + "BinOp")
        self.indent += 1
        print("  " * self.indent + "Left:")
        self.print_node(node.left)
        print("  " * self.indent + "Op: " + node.op.value)
        print("  " * self.indent + "Right:")
        self.print_node(node.right)
        self.indent -= 1

    def print_num(self, node):
        print("  " * self.indent + "Num: " + str(node.value))

    def print_unary(self, node):
        print("  " * self.indent + "Unary")
        self.indent += 1
        print("  " * self.indent + "Op: " + node.op.value)
        print("  " * self.indent + "Child:")
        self.print_node(node.child)
        self.indent -= 1

    def print_string(self, node):
        print("  " * self.indent + "String: " + node.value)
        if node.child:
            print("  " * self.indent + "Child:")
            self.print_node(node.child)

    def print_binbooleanop(self, node):
        print("  " * self.indent + "BinBooleanOp")
        self.indent += 1
        print("  " * self.indent + "Left:")
        self.print_node(node.left)
        print("  " * self.indent + "Op: " + node.op.value)
        print("  " * self.indent + "Right:")
        self.print_node(node.right)
        self.indent -= 1

    def print_unaryboolean(self, node):
        print("  " * self.indent + "UnaryBoolean")
        self.indent += 1
        print("  " * self.indent + "Op: " + str(node.op))
        print("  " * self.indent + "Child:")
        self.print_node(node.child)
        self.indent -= 1

    def print_boolean(self, node):
        print("  " * self.indent + "Boolean: " + str(node.value))

    def print_null(self, node):
        print("  " * self.indent + "Null: " + str(node.value))

    def print_scopedblock(self, node):
        print("  " * self.indent + "ScopedBlock")
        self.indent += 1
        print("  " * self.indent + "Block Name: " + node.block_name)
        print("  " * self.indent + "Statement List:")
        for statement in node.statement_list:
            self.print_node(statement)
        self.indent -= 1

    def print_block(self, node):
        print("  " * self.indent + "Block")
        self.indent += 1
        print("  " * self.indent + "Block Name: " + node.block_name)
        print("  " * self.indent + "Statement List:")
        for statement in node.statement_list:
            self.print_node(statement)
        self.indent -= 1

    def print_if(self, node):
        print("  " * self.indent + "If")
        self.indent += 1
        print("  " * self.indent + "Left Block:")
        self.print_node(node.left)
        if node.condition:
            print("  " * self.indent + "Condition:")
            self.print_node(node.condition)
        if node.right:
            print("  " * self.indent + "Right Block:")
            self.print_node(node.right)
        self.indent -= 1

    def print_while(self, node):
        print("  " * self.indent + "While")
        self.indent += 1
        print("  " * self.indent + "Condition:")
        self.print_node(node.condition)
        print("  " * self.indent + "Child Block:")
        self.print_node(node.child)
        self.indent -= 1

    def print_var(self, node):
        print("  " * self.indent + "Var: " + node.var_name)

    def print_varassign(self, node):
        print("  " * self.indent + "VarAssign")
        self.indent += 1
        print("  " * self.indent + "Left Var:")
        self.print_node(node.left)
        print("  " * self.indent + "Right Expr:")
        self.print_node(node.right)
        self.indent -= 1

    def print_finalassign(self, node):
        print("  " * self.indent + "FinalAssign")
        self.indent += 1
        print("  " * self.indent + "Left Var:")
        self.print_node(node.left)
        print("  " * self.indent + "Right Expr:")
        self.print_node(node.right)
        self.indent -= 1

    def print_varcompoundassign(self, node):
        print("  " * self.indent + "VarCompoundAssign")
        self.indent += 1
        print("  " * self.indent + "Left Var:")
        self.print_node(node.left)
        print("  " * self.indent + "Op: " + node.op.value)
        print("  " * self.indent + "Right Expr:")
        self.print_node(node.right)
        self.indent -= 1

    def print_varauto(self, node):
        print("  " * self.indent + "VarAuto")
        self.indent += 1
        print("  " * self.indent + "Op: " + node.op.value)
        print("  " * self.indent + "Child Var:")
        self.print_node(node.child)
        self.indent -= 1

    def print_parameter(self, node):
        print("  " * self.indent + "Parameter")
        self.indent += 1
        print("  " * self.indent + "Left Var:")
        self.print_node(node.left)
        print("  " * self.indent + "Right: " + str(node.right))
        self.indent -= 1

    def print_argument(self, node):
        print("  " * self.indent + "Argument")
        self.indent += 1
        print("  " * self.indent + "Left: " + str(node.left))
        print("  " * self.indent + "Right: " + str(node.right))
        self.indent -= 1

    def print_functionstmt(self, node):
        print("  " * self.indent + "FunctionStmt: " + node.func_name)
        self.indent += 1
        if node.left:
            print("  " * self.indent + "Parameters:")
            self.print_node(node.left)
        print("  " * self.indent + "Scoped Block:")
        self.print_node(node.right)
        self.indent -= 1

    def print_functioncall(self, node):
        print("  " * self.indent + "FunctionCall: " + node.func_name)
        self.indent += 1
        print("  " * self.indent + "Arguments:")
        self.print_node(node.child)
        self.indent -= 1

    def print_bincomp(self, node):
        print("  " * self.indent + "BinComp")
        self.indent += 1
        print("  " * self.indent + "Left:")
        self.print_node(node.left)
        print("  " * self.indent + "Op: " + node.op.value)
        print("  " * self.indent + "Right:")
        self.print_node(node.right)
        self.indent -= 1

    def print_ternary(self, node):
        print("  " * self.indent + "Ternary")
        self.indent += 1
        print("  " * self.indent + "Condition:")
        self.print_node(node.condition)
        print("  " * self.indent + "True Expr:")
        self.print_node(node.left)
        print("  " * self.indent + "False Expr:")
        self.print_node(node.right)
        self.indent -= 1

    def print_for(self, node):
        print("  " * self.indent + "For")
        self.indent += 1
        print("  " * self.indent + "Init Var:")
        self.print_node(node.init_var)
        print("  " * self.indent + "Condition:")
        self.print_node(node.condition)
        print("  " * self.indent + "Auto:")
        self.print_node(node.auto)
        print("  " * self.indent + "Block Node:")
        self.print_node(node.block_node)
        self.indent -= 1

    def print_return(self, node):
        print("  " * self.indent + "Return")
        self.indent += 1
        print("  " * self.indent + "Child:")
        self.print_node(node.child)
        self.indent -= 1

    def print_noop(self):
        print("  " * self.indent + "NoOp")