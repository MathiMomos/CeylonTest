from CeylonInterpreter.NodeVisitor.NodeVisitor import NodeVisitor
from CeylonInterpreter.Symbols.ScopedSymbolTable import ScopedSymbolTable
from CeylonInterpreter.Symbols.Symbol import FunctionSymbol, VarSymbol, FinalSymbol

class CeylonSemantic(NodeVisitor):
    def __init__(self):
        self.current_scope = None

    def visit_Program(self, node):

        print("***************************")
        print("ENTER SCOPE: PROGRAM")

        self.current_scope = ScopedSymbolTable(
            scope_name=node.program_name,
            scope_level=1,
            enclosing_scope=None
        )

        #self.current_scope.init_builtins()
        self.visit(node.block_node)

        print(self.current_scope)
        print("EXITING SCOPE: PROGRAM")
        print("***************************")

        self.current_scope = None

    def visit_FunctionStmt(self, node):

        func_name = node.func_name

        # Verifies that the function is not defined yet
        func_symbol = self.current_scope.lookup(func_name)

        if func_symbol is not None:
            raise Exception("%s is already defined" % func_name)

        # Creating the func_symbol
        func_symbol = FunctionSymbol(func_name=func_name)

        # Creating the scope of the function
        function_scope = ScopedSymbolTable(
            scope_name=func_name,
            scope_level=self.current_scope.scope_level+1,
            enclosing_scope=self.current_scope
        )

        # Adding the func_symbol to the current_scope
        self.current_scope.define(func_symbol)

        print("***************************")
        print("ENTER FUNCTION SCOPE:", func_name)

        # Entering to the function scope
        self.current_scope = function_scope

        print(self.current_scope)

        # Registering the formal params
        self.visit(node.left)

        # Getting the list of params for the func_symbol reference
        func_symbol.params = self.current_scope.get_symbols_list()

        # Storing the scoped block for the func_symbol
        func_symbol.scoped_block_node = node.right

        # Visiting the statements of the function
        self.visit(node.right) # visits the scoped block

        print(self.current_scope)
        print("EXITING FUNCTION SCOPE:", func_name)
        print("***************************")

        # Exiting the function scope
        self.current_scope = self.current_scope.enclosing_scope

    def visit_FunctionCall(self, node):

        func_symbol = self.current_scope.lookup(node.func_name)

        if func_symbol is None:
            raise Exception("Function '%s' is not defined" % node.func_name)

        if not isinstance(func_symbol, FunctionSymbol):
            raise Exception("'%s' is not callable" % node.func_name)

        node.func_symbol = func_symbol

        self.visit(node.child)

    def visit_If(self, node):
        if_scope = ScopedSymbolTable(
            scope_name="If",
            scope_level=self.current_scope.scope_level+1,
            enclosing_scope=self.current_scope
        )

        print("***************************")
        print("ENTER SCOPE: IF")

        self.current_scope = if_scope

        self.visit(node.condition) # expr
        self.visit(node.left) # Block of the conditional

        print(self.current_scope)
        print("EXITING SCOPE: IF")
        print("***************************")

        self.current_scope = self.current_scope.enclosing_scope

        self.visit(node.right) # next elif of else

    def visit_While(self, node):
        while_scope = ScopedSymbolTable(
            scope_name="While",
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope
        )

        print("***************************")
        print("ENTER SCOPE: WHILE")

        self.current_scope = while_scope

        self.visit(node.condition)
        self.visit(node.child)

        print(self.current_scope)
        print("EXITING SCOPE: WHILE")
        print("***************************")

        self.current_scope = self.current_scope.enclosing_scope

    def visit_For(self, node):
        for_scope = ScopedSymbolTable(
            scope_name="For",
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope
        )

        print("***************************")
        print("ENTER SCOPE: FOR")

        self.current_scope = for_scope

        self.visit(node.init_var)
        self.visit(node.condition)
        self.visit(node.auto)
        self.visit(node.block_node)

        print(self.current_scope)
        print("EXITING SCOPE: FOR")
        print("***************************")

        self.current_scope = self.current_scope.enclosing_scope

    def visit_Block(self, node):
        for statement in node.statement_list:
            self.visit(statement)

    def visit_ScopedBlock(self, node):
        for statement in node.statement_list:
            self.visit(statement)

    def visit_Parameter(self, node):

        # Param name for the VarSymbol
        param_name = node.left.var_name

        # Verifies if the symbol is currently saved
        saved_symbol = self.current_scope.lookup(param_name, current_scope_only=True)

        if saved_symbol is not None:
            # Raises an error if the symbol is already defined
            raise Exception("Local variable '%s' already exists" % param_name)

        # Saving the formal param
        param_symbol = VarSymbol(var_name=param_name)
        self.current_scope.define(param_symbol)

        # Next param or NoOp call
        self.visit(node.right)

    def visit_Argument(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_String(self, node):
        pass

    def visit_StringConcat(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Boolean(self, node):
        pass

    def visit_Null(self, node):
        pass

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Num(self, node):
        pass

    def visit_BinBooleanOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_BinComp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Unary(self, node):
        self.visit(node.child)

    def visit_UnaryBoolean(self, node):
        self.visit(node.child)

    def visit_Ternary(self, node):
        self.visit(node.condition)
        self.visit(node.left)
        self.visit(node.right)

    def visit_Print(self, node):
        self.visit(node.child)

    def visit_Scan(self, node):
        var_name = node.child.var_name

        # Verifies if the symbol is currently saved
        var_symbol = self.current_scope.lookup(var_name, current_scope_only=True)


        if var_symbol is not None:
            return

        var_symbol = VarSymbol(var_name=var_name)
        self.current_scope.define(var_symbol)

        self.visit(node.child)

    def visit_VarAssign(self, node):
        var_name = node.left.var_name
        var_symbol = self.current_scope.lookup(var_name)  # Finds at the scope and in the enclosing scope

        # Checks if the assign is for a final (Raises an Exception)
        if isinstance(var_symbol, FinalSymbol):
            raise Exception("Final '%s' cannot be reasigned" % var_name)

        if isinstance(var_symbol, FunctionSymbol):
            raise Exception("Function '%s' cannot be reassigned" % var_name)

        self.visit(node.right)

        if var_symbol is not None:
            return

        var_symbol = VarSymbol(var_name=var_name)
        self.current_scope.define(var_symbol)


    def visit_FinalAssign(self, node):
        final_name = node.left.var_name

        saved_final_symbol = self.current_scope.lookup(final_name)

        if isinstance(saved_final_symbol, VarSymbol):
            raise Exception("Var '%s' already exists" % final_name)

        # Raises a SemanticError if the final is already defined
        if isinstance(saved_final_symbol, FinalSymbol):
            raise Exception("Final '%s' already exists" % final_name)

        self.visit(node.right)

        final_symbol = FinalSymbol(final_name=final_name)
        self.current_scope.define(final_symbol)

    def visit_VarAuto(self, node):
        var_name = node.child.var_name
        var_symbol = self.current_scope.lookup(var_name)  # Finds at the scope and in the enclosing scope
        self.visit(node.child)

        if isinstance(var_symbol, FinalSymbol):
            raise Exception("Final '%s' cannot be reassigned" % var_name)

        if var_symbol is None:
            raise Exception("Variable '%s' is not defined" % var_name)

    def visit_Var(self, node):
        var_name = node.var_name
        var_symbol = self.current_scope.lookup(var_name) # Finds at the scope and in the enclosing scope

        if var_symbol is None:
            raise Exception("Variable '%s' is not defined" % var_name)

        return var_symbol.type

    def visit_VarCompoundAssign(self, node):
        var_name = node.left.var_name
        var_symbol = self.current_scope.lookup(var_name)  # Finds at the scope and in the enclosing scope

        if var_symbol is None:
            raise Exception("Variable '%s' is not defined" % var_name)

        if isinstance(var_symbol, FinalSymbol):
            raise Exception("Final '%s' cannot be reassigned" % var_name)

        self.visit(node.right)

    def visit_ConcatAssign(self, node):
        var_name = node.left.var_name
        var_symbol = self.current_scope.lookup(var_name) # Finds at the scope and in the enclosing scope

        if var_symbol is None:
            raise Exception("Variable '%s' is not defined" % var_name)

        if isinstance(var_symbol, FinalSymbol):
            raise Exception("Final '%s' cannot be reassigned" % var_name)

        self.visit(node.right)

    def visit_Return(self, node):
        self.visit(node.child)

    def visit_NoOp(self, node):
        pass