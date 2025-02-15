class Symbol:
    def __init__(self, name):
        self.name = name
        self.type = type

class VarSymbol(Symbol):
    def __init__(self, var_name):
        super().__init__(var_name)

    def __str__(self):
        s = "Var"
        return s

class FinalSymbol(Symbol):
    def __init__(self, final_name):
        super().__init__(final_name)

    def __str__(self):
        s = "Final"
        return s

class FunctionSymbol(Symbol):
    def __init__(self, func_name, params=None, scoped_block_node = None):
        super().__init__(func_name)
        self.params = params
        self.scoped_block_node = scoped_block_node

    def __str__(self):
        s = "Function"
        return s

#class BuiltinSymbol(Symbol):
#    def __init__(self, name):
#        super().__init__(name)
#
#    def __str__(self):
#        s = self.name
#        return s

#    __repr__ = __str__