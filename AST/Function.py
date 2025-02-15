class FunctionNode:
    pass

class Return(FunctionNode):
    def __init__(self, child):
        self.child = child

class Parameter(FunctionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right # Parameter

class Argument(FunctionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right # Argument

class FunctionStmt(FunctionNode):
    def __init__(self, func_name, left, right):
        self.left = left
        self.func_name = func_name
        self.right = right

class FunctionCall(FunctionNode):
    def __init__(self, func_name, child, func_symbol = None):
        self.func_name = func_name
        self.child = child
        self.func_symbol = func_symbol