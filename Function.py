from AST import AST, ScopeBlock
from Var import Var

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
    def __init__(self, func_name, right : ScopeBlock, left : Parameter = None):
        self.left = left
        self.func_name = func_name
        self.right = right

class FunctionCall(FunctionNode):
    def __init__(self, func_name, child : Argument):
        self.func_name = func_name
        self.child = child