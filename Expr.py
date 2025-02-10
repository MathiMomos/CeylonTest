from AST import AST
from TokenType import Token

class ExprNode(AST):
    pass

class BinOp(ExprNode):
    def __init__(self, left : AST, op : Token, right : AST):
        self.left = left
        self.op = op
        self.right = right
        
class Num(ExprNode):
    def __init__(self, value):
        self.value = value
        
class Unary(ExprNode):
    def __init__(self, op : Token, child : AST):
        self.op = op
        self.child = child
        
class String(ExprNode):
    def __init__(self, value, child = None):
        self.value = value
        self.child = child # String
        
class BinBooleanOp(ExprNode):
    def __init__(self, left : AST, op : Token, right : AST):
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
        
class Null(ExprNode):
    def __init__(self, value):
        self.value = value
