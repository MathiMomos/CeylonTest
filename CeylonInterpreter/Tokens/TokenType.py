from enum import Enum

class TokenType (Enum):
    
    # IDENTIFIER
    ID = None
    
    # LITERALS
    INTEGER = "INTEGER" # LEXER GIVES THE VALUE
    STRING = "STRING" # LEXER GIVES THE VALUE
    FSTRING = "FSTRING" # LEXER GIVES THE VALUE
    BOOLEAN = "BOOLEAN" # LEXER GIVES THE VALUE
    FLOAT = "FLOAT" # LEXER GIVES THE VALUE
    
    # ASSIGN OPTRS
    ASSIGN = "="
    PLUS_ASSIGN = "+="
    MINUS_ASSIGN = "-="
    TIMES_ASSIGN = "*="
    DIVIDE_ASSIGN = "/="
    POWER_ASSIGN = "**="
    MODULO_ASSIGN = "%="
    INT_DIVIDE_ASSIGN = "//="
    CONCAT_ASSIGN = "...="
    INCREMENT = "++"
    DECREMENT = "--"
    
    # RESERVED WORDS (WARNING: MAINTAIN THE ORDER)
    FINAL = 'final'
    IF = 'if'
    ELIF = 'elif'
    ELSE = 'else'
    FOR = "for"
    WHILE = "while"
    SWITCH = "switch"
    CASE = "case"
    DEFAULT = "default"
    RETURN = "return"
    FN = "fn"
    CLASS = "class"
    IN = "in"
    TRUE = "true"
    FALSE = "false"
    PRINT = "print"
    SCAN = "scan"
    NULL = "null"
    
    # LOGIC OPTRS
    AND = "&&"
    OR = "||"
    NOT = "!"
    
    # DELIMITERS
    LBRACE = "{"
    RBRACE = "}"
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    COMMA = ","
    DOT = "."
    SEMI = ";"
    
    # TERNARY
    TERNARY_Q = "?"
    TERNARY_C = ":"

    # CONCAT
    CONCAT = "..."

    # COMPARISON OPTRS
    EQ = "=="
    NE = "!="
    LT = "<"
    GT = ">"
    LE = "<="
    GE = ">="
    
    # ARITHMETIC OPTRS
    PLUS = "+"
    MINUS = "-"
    TIMES = "*"
    DIVIDE = "/"
    POWER = "**"
    MODULO = "%"
    INT_DIVIDE = "//"

    @staticmethod
    def generate_tokens():
        TokenTypeList = list(TokenType)
        token_list = [token.name for token in TokenTypeList]
        reserved_list = token_list[token_list.index("FINAL"):token_list.index("NULL")+1]
        reserved_tokens = {token.value: token.name for token in [TokenType[tokenInstance] for tokenInstance in reserved_list]}

        return token_list, reserved_tokens
    
class Token:
    def __init__(self, name, value):
        self.name = name
        self.value = value

tokens, reserved = TokenType.generate_tokens()