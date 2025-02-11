from lexer import CeylonLexer
from parser import Parser
import AST

text = \
'''
for (a = 1; a < 10; a++) {
  wasa += 10;  
}
'''

lexer = CeylonLexer()
lexer.build()
parser = Parser(lexer)
parser.build()
ast = parser.test(text)

printer = AST.ASTPrinter()
printer.print_node(ast)