class Symbol:
    def __init__(self, name, type="None"):
        self.name = name
        self.type = type

class VarSymbol(Symbol):
    def __init__(self, var_name, var_type):
        super().__init__(var_name, var_type)

    def __str__(self):
        s = self.type
        return s

class FinalSymbol(Symbol):
    def __init__(self, final_name, final_type):
        super().__init__(final_name, final_type)

    def __str__(self):
        s = self.type
        return s

class FunctionSymbol(Symbol):
    def __init__(self, func_name, params=None, scoped_block_node = None, func_type = "None"):
        super().__init__(func_name, func_type)
        self.params = params
        self.scoped_block_node = scoped_block_node

    def __str__(self):
        params = ""

        for param in self.params:
            params += param.__str__() + "\n"

        func_type = self.type + "\n"

        return func_type + params

class BuiltinSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        s = self.name
        return s

    __repr__ = __str__