class VarNode:
    pass

class Var(VarNode):
    def __init__(self, var_name):
        self.var_name = var_name

class VarAssign(VarNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class VarAuto(VarNode):
    def __init__(self, op, child):
        self.op = op
        self.child = child

class FinalAssign(VarNode):
    def __init__(self, left: Var, right):
        self.left = left
        self.right = right

class VarCompoundAssign(VarNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right