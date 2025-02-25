import ply.lex as lex
from CeylonInterpreter.Tokens.TokenType import TokenType, Token

class CeylonLexer:
    tokens, reserved = TokenType.generate_tokens()

    # Expresiones regulares para operadores
    # Operadores de asignación
    def t_POWER_ASSIGN(self, t):
        r'\*\*='
        t.value = Token(TokenType.POWER_ASSIGN.name, TokenType.POWER_ASSIGN.value)
        return t

    def t_PLUS_ASSIGN(self, t):
        r'\+='
        t.value = Token(TokenType.PLUS_ASSIGN.name, TokenType.PLUS_ASSIGN.value)
        return t

    def t_MINUS_ASSIGN(self, t):
        r'-='
        t.value = Token(TokenType.MINUS_ASSIGN.name, TokenType.MINUS_ASSIGN.value)
        return t

    def t_TIMES_ASSIGN(self, t):
        r'\*='
        t.value = Token(TokenType.TIMES_ASSIGN.name, TokenType.TIMES_ASSIGN.value)
        return t

    def t_DIVIDE_ASSIGN(self, t):
        r'/='
        t.value = Token(TokenType.DIVIDE_ASSIGN.name, TokenType.DIVIDE_ASSIGN.value)
        return t

    def t_MODULO_ASSIGN(self, t):
        r'%='
        t.value = Token(TokenType.MODULO_ASSIGN.name, TokenType.MODULO_ASSIGN.value)
        return t

    def t_INT_DIVIDE_ASSIGN(self, t):
        r'//='
        t.value = Token(TokenType.INT_DIVIDE_ASSIGN.name, TokenType.INT_DIVIDE_ASSIGN.value)
        return t

    def t_CONCAT_ASSIGN(self, t):
        r'\.\.\.='
        t.value = Token(TokenType.CONCAT_ASSIGN.name, TokenType.CONCAT_ASSIGN.value)
        return t

    def t_INCREMENT(self, t):
        r'\+\+'
        t.value = Token(TokenType.INCREMENT.name, TokenType.INCREMENT.value)
        return t

    def t_DECREMENT(self, t):
        r'--'
        t.value = Token(TokenType.DECREMENT.name, TokenType.DECREMENT.value)
        return t

    # Operadores aritméticos
    def t_POWER(self, t):
        r'\*\*'
        t.value = Token(TokenType.POWER.name, TokenType.POWER.value)
        return t

    def t_INT_DIVIDE(self, t):
        r'//'
        t.value = Token(TokenType.INT_DIVIDE.name, TokenType.INT_DIVIDE.value)
        return t

    def t_PLUS(self, t):
        r'\+'
        t.value = Token(TokenType.PLUS.name, TokenType.PLUS.value)
        return t

    def t_MINUS(self, t):
        r'-'
        t.value = Token(TokenType.MINUS.name, TokenType.MINUS.value)
        return t

    def t_TIMES(self, t):
        r'\*'
        t.value = Token(TokenType.TIMES.name, TokenType.TIMES.value)
        return t

    def t_DIVIDE(self, t):
        r'/'
        t.value = Token(TokenType.DIVIDE.name, TokenType.DIVIDE.value)
        return t

    def t_MODULO(self, t):
        r'%'
        t.value = Token(TokenType.MODULO.name, TokenType.MODULO.value)
        return t

        # Operador de concatenación
    def t_CONCAT(self, t):
        r'\.\.\.'
        t.value = Token(TokenType.CONCAT.name, TokenType.CONCAT.value)
        return t

        # Operadores de comparación
    def t_EQ(self, t):
        r'=='
        t.value = Token(TokenType.EQ.name, TokenType.EQ.value)
        return t

    def t_NE(self, t):
        r'!='
        t.value = Token(TokenType.NE.name, TokenType.NE.value)
        return t

    def t_LE(self, t):
        r'<='
        t.value = Token(TokenType.LE.name, TokenType.LE.value)
        return t

    def t_GE(self, t):
        r'>='
        t.value = Token(TokenType.GE.name, TokenType.GE.value)
        return t

    def t_LT(self, t):
        r'<'
        t.value = Token(TokenType.LT.name, TokenType.LT.value)
        return t

    def t_GT(self, t):
        r'>'
        t.value = Token(TokenType.GT.name, TokenType.GT.value)
        return t

    # Operadores lógicos
    def t_AND(self, t):
        r'&&'
        t.value = Token(TokenType.AND.name, TokenType.AND.value)
        return t

    def t_OR(self, t):
        r'\|\|'
        t.value = Token(TokenType.OR.name, TokenType.OR.value)
        return t

    def t_NOT(self, t):
        r'!'
        t.value = Token(TokenType.NOT.name, TokenType.NOT.value)
        return t

    # Operador ternario
    def t_TERNARY_Q(self, t):
        r'\?'
        t.value = Token(TokenType.TERNARY_Q.name, TokenType.TERNARY_Q.value)
        return t

    def t_TERNARY_C(self, t):
        r':'
        t.value = Token(TokenType.TERNARY_C.name, TokenType.TERNARY_C.value)
        return t

    # Operador de asignación básico
    def t_ASSIGN(self, t):
        r'='
        t.value = Token(TokenType.ASSIGN.name, TokenType.ASSIGN.value)
        return t

    # Símbolos
    def t_LBRACE(self, t):
        r'\{'
        t.value = Token(TokenType.LBRACE.name, TokenType.LBRACE.value)
        return t

    def t_RBRACE(self, t):
        r'\}'
        t.value = Token(TokenType.RBRACE.name, TokenType.RBRACE.value)
        return t

    def t_LPAREN(self, t):
        r'\('
        t.value = Token(TokenType.LPAREN.name, TokenType.LPAREN.value)
        return t

    def t_RPAREN(self, t):
        r'\)'
        t.value = Token(TokenType.RPAREN.name, TokenType.RPAREN.value)
        return t

    def t_LBRACKET(self, t):
        r'\['
        t.value = Token(TokenType.LBRACKET.name, TokenType.LBRACKET.value)
        return t

    def t_RBRACKET(self, t):
        r'\]'
        t.value = Token(TokenType.RBRACKET.name, TokenType.RBRACKET.value)
        return t

    def t_COMMA(self, t):
        r','
        t.value = Token(TokenType.COMMA.name, TokenType.COMMA.value)
        return t

    def t_DOT(self, t):
        r'\.'
        t.value = Token(TokenType.DOT.name, TokenType.DOT.value)
        return t

    def t_SEMI(self, t):
        r';'
        t.value = Token (TokenType.SEMI.name, TokenType.SEMI.value)
        return t

    # Reglas para literales y otros tokens complejos
    def t_NULL(self, t):
        r'\bNULL\b'
        t.value = Token(TokenType.NULL.name, TokenType.NULL.value)
        return t

    def t_BOOLEAN(self, t):
        r'true|false'
        t.value = Token(TokenType.BOOLEAN.name, t.value.lower() == 'true')
        return t

    def t_FLOAT(self, t):
        r'\d+\.\d+'
        t.value = Token(TokenType.FLOAT.name, float(t.value))
        return t

    def t_INTEGER(self, t):
        r'\d+'
        t.value = Token(TokenType.INTEGER.name, int(t.value))
        return t

    def t_FSTRING(self, t):
        r'f[\'"](?:[^\\\']|\\.)*?[\'"]'
        t.value = Token(TokenType.FSTRING.name, t.value[2:-1].replace('\\"', '"').replace("\\'", "'"))
        return t

    def t_STRING(self, t):
        r'[\'"](?:[^\\\']|\\.)*?[\'"]'
        t.value = Token(TokenType.STRING.name, t.value[1:-1].replace('\\"', '"').replace("\\'", "'"))
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'ID')
        t.value = Token(t.type, t.value)
        return t

    # Manejo de saltos de línea y errores
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Ignorar espacios y tabs
    t_ignore = ' \t'

    def t_error(self, t):
        print(f"Carácter ilegal '{t.value[0]}' en línea {t.lineno}")
        t.lexer.skip(1)

    # Comentarios
    def t_COMMENT_SINGLE(self, t):
        r'\#[^\n]*'
        pass

    # Construir el lexer
    def build(self):
        self.lexer = lex.lex(module=self)

    def test(self, input):
        self.lexer.input(input)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)