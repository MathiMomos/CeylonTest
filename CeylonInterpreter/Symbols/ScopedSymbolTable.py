from .Symbol import BuiltinSymbol

class ScopedSymbolTable:
    def __init__(self, scope_name, scope_level, enclosing_scope):
        self._symbols = dict()
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope

    def init_builtins(self):
        self.define(BuiltinSymbol("Number"))
        self.define(BuiltinSymbol("String"))
        self.define(BuiltinSymbol("Boolean"))
        self.define(BuiltinSymbol("Null"))

    def define(self, symbol):
        self._symbols[symbol.name] = symbol

    def lookup(self, symbol_name, current_scope_only=False):
        symbol = self._symbols.get(symbol_name)

        if symbol is not None:
            return symbol

        if current_scope_only:
            return None

        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(symbol_name) # only one plus level of search

    def get_symbols_list(self):
        return list(self._symbols.values())

    def __str__(self):
        main = \
'''
Symbol table: {}
Scope level: {}
Parent: {}
        
Symbols:
'''.format(
            self.scope_name,
            self.scope_level,
            self.enclosing_scope.scope_name if self.enclosing_scope is not None else "None",
        )

        symbols = ""

        for symbol_name, symbol in self._symbols.items():
            symbols += "{}: {}\n".format(symbol_name, symbol.type)

        return main + symbols

    __repr__ = __str__