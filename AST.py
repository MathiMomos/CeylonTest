from TokenType import Token
from Expr import BinBooleanOp

class AST():
    pass

class ScopeBlock(AST):
    def __init__(self, block_name, statement_list = []):
        self.block_name = block_name
        self.statement_list = statement_list

class Block(AST):
    def __init__(self, block_name, statement_list = []):
        self.block_name = block_name
        self.statement_list = statement_list

class If(AST):
    def __init__(self, left : Block, condition : BinBooleanOp = None, right : If = None):
        self.left = left
        self.condition = condition
        self.right = right

class While(AST):
    def __init__(self, condition : BinBooleanOp, child : Block):
        self.condition = condition
        self.child = child