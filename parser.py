import ply.yacc as yacc
from lexer import Lexer
from AST import ScopeBlock, Block, If, While
from Expr import ExprNode, Null, BinBooleanOp, Boolean, UnaryBoolean, String, Num, BinOp, Unary
from TokenType import TokenType, Token
from Var import Var, VarCompoundAssign, VarAssign, FinalAssign, VarAuto
from Function import Parameter, Argument, FunctionStmt, FunctionCall


class Parser():
    
    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', "INT_DIVIDE"),
        ('right', 'POWER'),
    )
    
    def __init__(self, lexer : Lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens

    ####
    #### SCOPE BLOCK RULES
    ####

    def p_scope_block(self, p):
        '''scope_block : statement_list
                       | empty'''
        block_name = "ScopeBlock"
        statement_list = p[1]

        p[0] = ScopeBlock(block_name=block_name, statement_list=statement_list)

    ####
    #### BLOCK RULES
    ####

    def p_block(self, p):
        '''block : statement_list
                 | empty'''
        block_name = "Block"
        statement_list = p[1]

        p[0] = Block(block_name=block_name, statement_list=statement_list)

    def p_statement_list(self, p):
        '''statement_list : statement SEMI statement_list
                          | empty'''
        len_rule = len(p)

        if len_rule == 4:
            p[0] = p[1] + [p[2]] # statement list: [AST nodes, None]
        else:
            p[0] = [p[1]] # [None]

    def p_statement(self, p):
        '''statement : var_assign
                     | final_assign
                     | var_compound_assign
                     | var_auto
                     | expr
                     | func_stmt
                     | func_call
                     | if_stmt
                     | while_stmt
                     | empty'''
        p[0] = p[1] # None or AST NODE

    ####
    #### FUNCTION RULES
    ####

    def p_func_stmt(self, p):
        '''func_stmt : FN var LPAREN parameters_list RPAREN LBRACE scoped_block RBRACE'''
        func_name = p[2].value
        left: Parameter = p[4] # Possibly None: No parameters
        right: ScopeBlock = p[7]

        p[0] = FunctionStmt(left=left, func_name=func_name, right=right)
    
    def p_func_call(self, p):
        '''func_call : var LPAREN arguments_list RPAREN'''
        func_name = p[1].value
        child : Argument = p[3]

        p[0] = FunctionCall(func_name=func_name, child=child)

    def p_arguments_list(self, p):
        '''arguments_list : non_empty_arguments_list
                           | empty'''
        p[0] = p[1]  # None or Argument

    def p_parameters_list(self, p):
        '''parameters_list : non_empty_parameters_list
                           | empty'''
        p[0] = p[1] # None or Parameter

    def p_non_empty_parameters_list(self, p):
        '''non_empty_parameters_list : var COMMA parameters_list
                                     | var'''
        len_rule = len(p)

        if len_rule == 4:
            left : Var = p[1]
            right : Parameter = p[3]
            p[0] = Parameter(left=left, right=right)
        else:
            p[0] = p[1]

    ####
    #### FLOW CONTROL RULES
    ####

    #### CONDITIONAL RULES

    # IF RULES

    def p_if_stmt(self, p):
        '''if_stmt : IF LPAREN bool_expr RPAREN LBRACE block RBRACE elif_stmt'''
        condition : BinBooleanOp = p[3]
        left : Block = p[6]
        right : If = p[8]

        p[0] = If(left=left, condition=condition, right=right)
    
    def p_elif_stmt(self, p):
        '''elif_stmt : ELIF LPAREN bool_expr RPAREN LBRACE block RBRACE elif_stmt
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
        p[0] = If(left=left)

    #### LOOP RULES

    # WHILE RULES

    def p_while_stmt(self, p):
        '''while_stmt : WHILE LPAREN bool_expr RPAREN LBRACE block RBRACE'''
        condition : BinBooleanOp = p[3]
        child : Block = p[6]
        p[0] = While(condition=condition, child=child)

    def p_for_stmt(self, p):
        '''for_stmt : FOR LPAREN var_assign SEMI bool_expr SEMI var_auto RPAREN LBRACE scoped_block RBRACE'''
        pass

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
        right : BinOp = p[3]
        p[0] = VarCompoundAssign(left=left, op=op, right=right)

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
        '''expr : num_expr
                | string_expr
                | boolean_expr
                | null_expr
                | ternary_expr'''
        p[0] = p[1]
    
    #### ARITHMETIC RULES

    def p_num_factor(self, p):
        '''num_factor : PLUS num_factor
                      | MINUS num_factor
                      | INTEGER
                      | FLOAT
                      | LPAREN expr RPAREN
                      | var'''
        len_rule = len(p)

        if len_rule == 3:
            op : Token = p[1]
            child = p[2]
            p[0] = Unary(op=op, child=child)
        elif len_rule == 2:
            token_terminal : Token = p[1]
            if token_terminal.name == TokenType.ID.name:
                p[0] = Var(var_name=token_terminal.value)
            else:
                p[0] = Num(value=token_terminal.value)
        else:
            p[0] = p[2]

    
    def p_num_expr(self, p):
        '''num_expr : expr PLUS expr
                    | expr MINUS expr
                    | expr TIMES expr
                    | expr DIVIDE expr
                    | expr INT_DIVIDE expr
                    | expr POWER expr
                    | num_factor'''
        len_rule = len(p)

        if len_rule == 4:
            left = p[1]
            op : Token = p[2]
            right = p[3]

            p[0] = BinOp(left=left, op=op, right=right)
        else:
            node = p[1]
            p[0] = p[1]
    
    def p_string_expr(self, p):
        '''string_expr : STRING PLUS string_expr
                       | STRING'''
        len_rule = len(p)

        if len_rule == 4:
            token_terminal: Token = p[1]
            node : String = p[3]
            p[0] = String(value=token_terminal.value, child=node)
        else:
            token_terminal : Token = p[1]
            p[0] = String(value=token_terminal.value)

    
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
                          | var'''
        grouping = 4
        len_rule = len(p)

        if len_rule == grouping:
            bin_bool_node: BinBooleanOp = p[2]
            p[0] = bin_bool_node
        else:
            token_terminal : Token = p[1]
            if token_terminal.name == TokenType.BOOLEAN.name:
                p[0] = Boolean(value=token_terminal.value)
            elif token_terminal.name == TokenType.ID.name:
                p[0] = Var(var_name=token_terminal.value)

    #### NULL RULES
    
    def p_null_expr(self, p):
        '''null_expr : NULL'''
        token_null : Token = p[1]
        p[0] = Null(value=token_null.value)
    
    ####
    #### SPECIAL RULES
    ####

    def ternary_expr(self, p):
        '''ternary_expr : boolean_expr TERNARY_Q expr TERNARY_C expr'''
        pass

    def p_empty(self, p):
        '''empty : '''
        p[0] = None
    
    ################################

    def p_error(self, p):
        print("Syntax error in input!")
    
    def build(self):
        self.parser = yacc.yacc(module=self)
        
    def test(self, input):
        return self.parser.parse(input)