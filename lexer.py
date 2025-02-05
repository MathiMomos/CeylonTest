import ply.lex as lex

class Lexer():
    
    reserved = {
    'final': 'FINAL',
    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'switch': 'SWITCH',
    'case': 'CASE',
    'fn': 'FN',
    'class': 'CLASS',
    'true': 'TRUE',
    'false': 'FALSE',
    'NULL': 'NULL'
    }
    
    assign_oprs = [
        # Operadores de asignación
        'ASSIGN',          # =
        'PLUS_ASSIGN',     # +=
        'MINUS_ASSIGN',    # -=
        'TIMES_ASSIGN',    # *=
        'DIVIDE_ASSIGN',   # /=
        'POWER_ASSIGN',    # **=
        'MODULO_ASSIGN',   # %=
        'INT_DIVIDE_ASSIGN', # //=
        'INCREMENT',       # ++
        'DECREMENT',       # --
    ]
    
    logic_oprs = [
        # Operadores lógicos
        'AND',             # &&
        'OR',              # ||
        'NOT',             # !
    ]
    
    delimiters = [
        # Delimitadores
        'LBRACE',          # {
        'RBRACE',          # }
        'LPAREN',          # (
        'RPAREN',          # )
        'LBRACKET',        # [
        'RBRACKET',        # ]
        'COMMA',           # ,
        'DOT',             # .
        'SEMI',            # ;
    ]
    
    ternary = [
        # Operador ternario
        'TERNARY_Q',       # ?
        'TERNARY_C',       # :
    ]
    
    comparison_oprs = [
        # Operadores de comparación
        'EQ',              # ==
        'NE',              # !=
        'LT',              # <
        'GT',              # >
        'LE',              # <=
        'GE',              # >=
    ]
    
    arithmetic_oprs = [
         # Operadores aritméticos
        'PLUS',            # +
        'MINUS',           # -
        'TIMES',           # *
        'DIVIDE',          # /
        'POWER',           # **
        'MODULO',          # %
        'INT_DIVIDE',      # //
    ]
    
    tokens = [
    # Identificadores y literales
    'INTEGER', 'STRING', 'FSTRING', 'ID', 'BOOLEAN', 'FLOAT',     
    ] + list(reserved.values()) + arithmetic_oprs + logic_oprs + assign_oprs + comparison_oprs + delimiters + ternary

    # Expresiones regulares para operadores
    # Operadores de asignación
    t_POWER_ASSIGN = r'\*\*='
    t_PLUS_ASSIGN = r'\+='
    t_MINUS_ASSIGN = r'-='
    t_TIMES_ASSIGN = r'\*='
    t_DIVIDE_ASSIGN = r'/='
    t_MODULO_ASSIGN = r'%='
    t_INT_DIVIDE_ASSIGN = r'//='
    t_INCREMENT = r'\+\+'
    t_DECREMENT = r'\-\+'

    # Operadores aritméticos
    t_POWER = r'\*\*'
    t_INT_DIVIDE = r'//'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MODULO = r'%'

    # Operadores lógicos
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_NOT = r'!'

    # Operadores de comparación
    t_EQ = r'=='
    t_NE = r'!='
    t_LE = r'<='
    t_GE = r'>='
    t_LT = r'<'
    t_GT = r'>'

    # Operador ternario
    t_TERNARY_Q = r'\?'
    t_TERNARY_C = r':'

    # Operador de asignación básico
    t_ASSIGN = r'='

    # Símbolos
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_COMMA = r','
    t_DOT = r'\.'
    t_SEMI = r';'

    # Ignorar espacios y tabs
    t_ignore = ' \t'

    # Reglas para literales y otros tokens complejos
    def t_NULL(self, t):
        r'\bNULL\b'
        t.value = None
        return t

    def t_BOOLEAN(self, t):
        r'true|false'
        t.value = (t.value.lower() == 'true')
        return t

    def t_FLOAT(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_FSTRING(self, t):
        r'f[\'"](?:[^\\\']|\\.)*?[\'"]'
        t.value = t.value[2:-1].replace('\\"', '"').replace("\\'", "'")
        return t

    def t_STRING(self, t):
        r'[\'"](?:[^\\\']|\\.)*?[\'"]'
        t.value = t.value[1:-1].replace('\\"', '"').replace("\\'", "'")
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    # Manejo de saltos de línea y errores
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Carácter ilegal '{t.value[0]}' en línea {t.lineno}")
        t.lexer.skip(1)

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