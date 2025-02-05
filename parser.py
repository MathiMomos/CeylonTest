import ply.yacc as yacc
from lexer import Lexer
from AST import BinOp, Number, UnaryOp, VarAssign, Var, print_ast

class Parser():
    
    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', "INT_DIVIDE"),
        ('right', 'POWER'),
    )
    
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens

    # VAR
    def p_var_assign(self, p):
        '''var_assign : var ASSIGN expr
                      | var PLUS_ASSIGN expr
                      | var MINUS_ASSIGN expr
                      | var TIMES_ASSIGN expr
                      | var DIVIDE_ASSIGN expr
                      | var POWER_ASSIGN expr
                      | var MODULO_ASSIGN expr
                      | var INT_DIVIDE_ASSIGN expr'''
        p[0] = VarAssign(p[1], p[2], p[3])

    def p_final_var_assign(self, p):
        '''var_assign : final_var ASSIGN expr
                      | final_var PLUS_ASSIGN expr
                      | final_var MINUS_ASSIGN expr
                      | final_var TIMES_ASSIGN expr
                      | final_var DIVIDE_ASSIGN expr
                      | final_var POWER_ASSIGN expr
                      | final_var MODULO_ASSIGN expr
                      | final_var INT_DIVIDE_ASSIGN expr'''
        p[0] = VarAssign(p[1], p[2], p[3])

    def p_var(self, p):
        '''var : ID'''
        p[0] = Var(name=p[1])

    def p_final_var(self, p):
        '''final_var : FINAL ID'''
        p[0] = Var(type="FINAL", name=p[2])

    # EXPR
    def p_expr(self, p):
        '''expr : expr PLUS expr
                | expr MINUS expr
                | expr TIMES expr
                | expr DIVIDE expr
                | expr INT_DIVIDE expr  
                | expr POWER expr
                | factor'''
        if len(p) == 4:
            p[0] = BinOp(p[1], p[2], p[3])
        else:
            p[0] = p[1]
        

    def p_factor(self, p):
        '''factor : PLUS factor
                  | MINUS factor
                  | INTEGER
                  | FLOAT
                  | LPAREN expr RPAREN
                  | var'''
        if len(p) == 3:
            if p[1] in ("+", "-"):
                p[0] = UnaryOp(p[1], p[2])
            else:
                p[0] = p[2]
        else:
            if isinstance(p[1], Var):
                p[0] = p[1]
            else:
                p[0] = Number(p[1])

    def p_error(self, p):
        print("Syntax error in input!")
    
    def build(self):
        self.parser = yacc.yacc(module=self)
        
    def test(self, input):
        return self.parser.parse(input)
    
lexer = Lexer()
lexer.build()
parser = Parser(lexer)
parser.build()
tree = parser.test("")
print_ast(tree)