from CeylonInterpreter.AR.Member import Number_type, String_type, Boolean_type, Null_type

class ExprNode:
    pass

class BinOp(ExprNode):
    def __init__(self, left, op, right): # op is a Token instance
        self.left = left
        self.op = op
        self.right = right

class Num(ExprNode):
    def __init__(self, value):
        self.value = value
        self.type = Number_type

class StringConcat(ExprNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class String(ExprNode):
    def __init__(self, value):
        self.value = value
        self.type = String_type

class Unary(ExprNode):
    def __init__(self, op, child): # op is a Token instance
        self.op = op
        self.child = child

class BinBooleanOp(ExprNode):
    def __init__(self, left, op, right): # op is a Token instance
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
        self.type = Boolean_type

class BinComp(ExprNode):
    def __init__(self, left, op, right): # op is a Token instance
        self.left = left
        self.op = op
        self.right = right

class Ternary(ExprNode):
    def __init__(self, left, condition, right):
        self.left = left # true expr
        self.condition = condition
        self.right = right # false expr

class Null(ExprNode):
    def __init__(self, value):
        self.value = value
        self.type = Null_type

class ToStr (ExprNode):
    def __init__(self, child):
        self.child = child

class ToNum (ExprNode):
    def __init__(self, child):
        self.child = child