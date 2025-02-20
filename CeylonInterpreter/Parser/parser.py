import ply.yacc as yacc
from AST.Program import *
from AST.Expr import *
from AST.Var import *
from AST.Block import *
from AST.Function import *
from AST.Special import *
from AST.Flow import *
from CeylonInterpreter.Tokens.TokenType import TokenType, Token

class Parser:
    
    def __init__(self):
        from CeylonInterpreter.Lexer.lexer import CeylonLexer
        lexer = CeylonLexer()
        lexer.build()
        self.parser = None
        self.Lexer = lexer
        self.tokens = lexer.tokens
        self.precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', "INT_DIVIDE"),
        ('right', 'POWER'),
    )

    ####
    #### PROGRAM RULES
    ####

    def p_program(self, p):
        '''program : block'''
        program_name = "Program"
        block_node = p[1]

        p[0] = Program(program_name=program_name, block_node=block_node)

    ####
    #### BLOCK RULES
    ####

    def p_block(self, p):
        '''block : statement_list'''
        p[1].reverse()
        statement_list = p[1]

        p[0] = Block(statement_list=statement_list)

    def p_statement_list(self, p):
        '''statement_list : statement statement_list
                          | empty'''

        len_rule = len(p)
        if len_rule == 3:
            p[0] = p[2] + [p[1]] # statement list: [AST nodes, NoOp]
        else:
            p[0] = [p[1]] # [NoOp]

    def p_statement(self, p):
        '''statement : var_assign SEMI
                     | final_assign SEMI
                     | var_compound_assign SEMI
                     | concat_assign SEMI
                     | var_auto SEMI
                     | expr SEMI
                     | func_stmt
                     | if_stmt
                     | while_stmt
                     | for_stmt
                     | print_stmt SEMI
                     | empty'''
        p[0] = p[1] # None or AST NODE

    ####
    #### SCOPE BLOCK RULES
    ####

    def p_scoped_block(self, p):
        '''scoped_block : scoped_statement_list'''
        p[1].reverse()
        statement_list = p[1]

        p[0] = ScopedBlock(statement_list=statement_list)

    def p_scope_statement_list(self, p):
        '''scoped_statement_list : scoped_statement scoped_statement_list
                                 | empty'''

        len_rule = len(p)
        if len_rule == 3:
            p[0] = p[2] + [p[1]] # statement list: [AST nodes, NoOp]
        else:
            p[0] = [p[1]] # [NoOp]

    def p_scope_statement(self, p):
        '''scoped_statement : var_assign SEMI
                            | final_assign SEMI
                            | var_compound_assign SEMI
                            | concat_assign SEMI
                            | var_auto SEMI
                            | expr SEMI
                            | func_stmt
                            | scoped_if_stmt
                            | scoped_while_stmt
                            | scoped_for_stmt
                            | print_stmt SEMI
                            | return SEMI
                            | empty'''
        p[0] = p[1] # None or AST NODE

    def p_return(self, p):
        '''return : RETURN expr'''

        node = p[2]
        p[0] = Return(child=node)

    ####
    #### FUNCTION RULES
    ####

    def p_func_stmt(self, p):
        '''func_stmt : FN var LPAREN parameters_list RPAREN LBRACE scoped_block RBRACE'''
        func_name = p[2].var_name
        left: Parameter = p[4] # Possibly None: No parameters
        right: ScopedBlock = p[7]

        p[0] = FunctionStmt(left=left, func_name=func_name, right=right)
    
    def p_func_call(self, p):
        '''func_call : var LPAREN arguments_list RPAREN'''
        func_name = p[1].var_name
        child : Argument = p[3]

        p[0] = FunctionCall(func_name=func_name, child=child)

    def p_arguments_list(self, p):
        '''arguments_list : non_empty_arguments_list
                          | empty'''
        p[0] = p[1]  # None o Argument

    def p_non_empty_arguments_list(self, p):
        '''non_empty_arguments_list : expr COMMA non_empty_arguments_list
                                    | expr'''  # <--- Cambio aquí
        len_rule = len(p)

        if len_rule == 4:
            left = p[1]
            right = p[3]
            p[0] = Argument(left=left, right=right)
        else:
            p[0] = Argument(left=p[1], right=NoOp())

    def p_parameters_list(self, p):
        '''parameters_list : non_empty_parameters_list
                           | empty'''
        p[0] = p[1] # None or Parameter

    def p_non_empty_parameters_list(self, p):
        '''non_empty_parameters_list : var COMMA non_empty_parameters_list
                                     | var'''
        len_rule = len(p)

        if len_rule == 4:
            left : Var = p[1]
            right : Parameter = p[3]
            p[0] = Parameter(left=left, right=right)
        else:
            p[0] = Parameter(left=p[1], right= NoOp())

    ####
    #### FLOW CONTROL RULES
    ####

    #### CONDITIONAL RULES

    # IF RULES

    def p_if_stmt(self, p):
        '''if_stmt : IF LPAREN boolean_expr RPAREN LBRACE block RBRACE elif_stmt'''
        condition : BinBooleanOp = p[3]
        left : Block = p[6]
        right : If = p[8]

        p[0] = If(left=left, condition=condition, right=right)
    
    def p_elif_stmt(self, p):
        '''elif_stmt : ELIF LPAREN boolean_expr RPAREN LBRACE block RBRACE elif_stmt
                     | else_stmt
                     | empty'''
        len_rule = len(p)

        if len_rule == 2:
            p[0] = p[1]
        else:
            condition: BinBooleanOp = p[3]
            left: Block = p[6]
            right: If = p[8]

            p[0] = If(left=left, condition=condition, right=right)

    def p_else_stmt(self, p):
        '''else_stmt : ELSE LBRACE block RBRACE'''
        left : Block = p[3]
        p[0] = If(condition=NoOp(), left=left, right=NoOp())

    # scoped structures

    def p_scoped_if_stmt(self, p):
        '''scoped_if_stmt : IF LPAREN boolean_expr RPAREN LBRACE scoped_block RBRACE scoped_elif_stmt'''
        condition: BinBooleanOp = p[3]
        left: Block = p[6]
        right: If = p[8]

        p[0] = If(left=left, condition=condition, right=right)

    def p_scoped_elif_stmt(self, p):
        '''scoped_elif_stmt : ELIF LPAREN boolean_expr RPAREN LBRACE scoped_block RBRACE scoped_elif_stmt
                     | scoped_else_stmt
                     | empty'''
        len_rule = len(p)

        if len_rule == 2:
            p[0] = p[1]
        else:
            condition: BinBooleanOp = p[3]
            left: Block = p[6]
            right: If = p[8]

            p[0] = If(left=left, condition=condition, right=right)

    def p_scoped_else_stmt(self, p):
        '''scoped_else_stmt : ELSE LBRACE scoped_block RBRACE'''
        left : Block = p[3]
        p[0] = If(condition=NoOp(), left=left, right=NoOp())

    def p_scoped_while_stmt(self, p):
        '''scoped_while_stmt : WHILE LPAREN boolean_expr RPAREN LBRACE scoped_block RBRACE'''
        condition : BinBooleanOp = p[3]
        child : Block = p[6]
        p[0] = While(condition=condition, child=child)

    def p_scoped_for_stmt(self, p):
        '''scoped_for_stmt : FOR LPAREN var_assign SEMI boolean_expr SEMI var_auto RPAREN LBRACE scoped_block RBRACE'''
        init_var : VarAssign = p[3]
        condition : BinBooleanOp = p[5]
        auto : VarAuto = p[7]
        block_node = p[10]
        p[0] = For(init_var=init_var, condition=condition, auto=auto, block_node=block_node)

    #### PRINT RULES

    def p_print_stmt(self, p):
        '''print_stmt : PRINT LPAREN expr RPAREN'''
        p[0] = Print(child=p[3])

    #### LOOP RULES

    # WHILE RULES

    def p_while_stmt(self, p):
        '''while_stmt : WHILE LPAREN boolean_expr RPAREN LBRACE block RBRACE'''
        condition : BinBooleanOp = p[3]
        child : Block = p[6]
        p[0] = While(condition=condition, child=child)

    def p_for_stmt(self, p):
        '''for_stmt : FOR LPAREN var_assign SEMI boolean_expr SEMI var_auto RPAREN LBRACE block RBRACE'''
        init_var : VarAssign = p[3]
        condition : BinBooleanOp = p[5]
        auto : VarAuto = p[7]
        block_node = p[10]
        p[0] = For(init_var=init_var, condition=condition, auto=auto, block_node=block_node)

    ####
    #### VAR RULES
    ####

    def p_var(self, p):
        '''var : ID'''
        token_terminal : Token = p[1]
        p[0] = Var(var_name=token_terminal.value)

    def p_var_assign(self, p):
        '''var_assign : var ASSIGN expr'''
        left: Var = p[1]
        right: ExprNode = p[3]
        p[0] = VarAssign(left=left, right=right)

    def p_final_assign(self, p):
        '''final_assign : FINAL var ASSIGN expr'''
        left : Var = p[2]
        right : ExprNode = p[4]
        p[0] = FinalAssign(left=left, right=right)

    def p_compound_assign(self, p):
        '''var_compound_assign : var PLUS_ASSIGN num_expr
                               | var MINUS_ASSIGN num_expr
                               | var TIMES_ASSIGN num_expr
                               | var DIVIDE_ASSIGN num_expr
                               | var POWER_ASSIGN num_expr
                               | var MODULO_ASSIGN num_expr
                               | var INT_DIVIDE_ASSIGN num_expr'''

        left : Var = p[1]
        op : Token = p[2]
        right = p[3]
        p[0] = VarCompoundAssign(left=left, op=op, right=right)

    def p_concat_assign(self, p):
        '''concat_assign : var CONCAT_ASSIGN string_expr'''
        left : Var = p[1]
        right = p[3]
        p[0] = ConcatAssign(left=left, right=right)

    def p_var_auto(self, p):
        '''var_auto : var INCREMENT
                    | var DECREMENT'''
        op : Token = p[2]
        child : Var = p[1]
        p[0] = VarAuto(op=op, child=child)

    ####
    #### EXPR RULES
    ####
    
    def p_expr(self, p):
        '''expr : string_expr
                | num_expr
                | boolean_expr
                | null_expr
                | ternary_expr
                | var
                | func_call'''
        p[0] = p[1]

    #### ARITHMETIC RULES|

    def p_num_factor(self, p):
        '''num_factor : PLUS num_factor
                      | MINUS num_factor
                      | INTEGER
                      | FLOAT
                      | LPAREN num_expr RPAREN
                      | func_call
                      | var'''
        len_rule = len(p)

        if len_rule == 3:
            op : Token = p[1]
            child = p[2]
            p[0] = Unary(op=op, child=child)
        elif len_rule == 2:
            factor = p[1]
            if isinstance(factor, Token):
                p[0] = Num(value=factor.value)
            else:
                p[0] = p[1]

        else:
            p[0] = p[2]

    def p_num_expr(self, p):
        '''num_expr : num_expr PLUS num_expr
                    | num_expr MINUS num_expr
                    | num_expr TIMES num_expr
                    | num_expr DIVIDE num_expr
                    | num_expr INT_DIVIDE num_expr
                    | num_expr POWER num_expr
                    | num_expr MODULO num_expr
                    | num_factor'''
        len_rule = len(p)

        if len_rule == 4:
            left = p[1]
            op: Token = p[2]
            right = p[3]

            p[0] = BinOp(left=left, op=op, right=right)
        else:
            node = p[1]
            p[0] = p[1]

    def p_string_expr(self, p):
        '''string_expr : string_expr CONCAT string_expr
                       | STRING
                       | var'''
        len_rule = len(p)

        if len_rule == 4:
                left = p[1]
                right = p[3]
                p[0] = StringConcat(left=left, right=right)
        else:
                factor = p[1]

                if isinstance(factor, Token):
                    p[0] = String(value=factor.value)
                else:
                    p[0] = p[1]# Var

    #### BOOLEAN RULES
    
    def p_boolean_expr(self, p):
        '''boolean_expr : boolean_expr AND boolean_expr
                        | boolean_expr OR boolean_expr
                        | NOT boolean_expr
                        | boolean_factor'''
        len_rule = len(p)

        if len_rule == 4:
            left = p[1]
            op : Token = p[2]
            right = p[3]
            p[0] = BinBooleanOp(left, op, right)
        elif len_rule == 3:
            token_not = p[1]
            node = p[2]
            p[0] = UnaryBoolean(op=token_not, child=node)
        else:
            node = p[1]
            p[0] = node
            
    
    def p_boolean_factor(self, p):
        '''boolean_factor : LPAREN boolean_expr RPAREN
                          | BOOLEAN
                          | comparison
                          | var'''
        grouping = 4
        len_rule = len(p)

        if len_rule == grouping:
            bin_bool_node: BinBooleanOp = p[2]
            p[0] = bin_bool_node
        else:
            factor = p[1]
            if isinstance(factor, BinComp) or isinstance(factor, Var):
                p[0] = factor
            elif factor.name == TokenType.BOOLEAN.name:
                p[0] = Boolean(value=factor.value)

    def p_comparison(self, p):
        '''comparison : expr EQ expr
                      | expr NE expr
                      | expr LT expr
                      | expr GT expr
                      | expr LE expr
                      | expr GE expr'''
        left : ExprNode = p[1]
        op : Token = p[2]
        right : ExprNode = p[3]

        p[0] = BinComp(left=left, op=op, right=right)

    #### NULL RULES

    def p_null_expr(self, p):
        '''null_expr : NULL'''
        token_null : Token = p[1]
        p[0] = Null(value=token_null.value)
    
    ####
    #### SPECIAL RULES
    ####

    def p_ternary_expr(self, p):
        '''ternary_expr : boolean_expr TERNARY_Q expr TERNARY_C expr'''
        left : ExprNode = p[3]
        condition = p[1]
        right : ExprNode = p[5]

        p[0] =Ternary(left=left, condition=condition, right=right)

    def p_empty(self, p):
        '''empty : '''
        p[0] = NoOp()
    
    ################################

    def p_error(self, p):
        print("Syntax error in input!:", p)
    
    def build(self):
        self.parser = yacc.yacc(module=self)
        
    def test(self, text):
        return self.parser.parse(text)