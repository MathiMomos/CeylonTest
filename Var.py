from AST import AST
from Expr import ExprNode
from TokenType import Token

class VarNode(AST):
    pass

class Var(VarNode):
    def __init__(self, var_name):
        self.var_name = var_name
        
class VarAssign(VarNode):
    def __init__(self, left : Var, right : ExprNode):
        self.left = left
        self.right = right
        
class FinalAssign(VarNode):
    def __init__(self, left : Var, right : ExprNode):
        self.left = left
        self.right = right
        
class VarCompoundAssign(VarNode):
    def __init__(self, left : Var, op : Token, right : ExprNode):
        self.left = left
        self.op = op
        self.right = right

class VarAuto(VarNode):
    def __init__(self, op : Token, child : Var):
        self.op = op
        self.child = child