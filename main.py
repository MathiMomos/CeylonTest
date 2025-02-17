from CeylonInterpreter.Parser.parser import Parser
from CeylonInterpreter.Semantic.semantic import CeylonSemantic

text = \
'''
x = 23;
y += 24;
'''

parser = Parser()
parser.build()
ast = parser.test(text)

semantic = CeylonSemantic()
semantic.visit(ast)
#printer = ASTPrinter()
#printer.print_node(ast)
