from CeylonInterpreter.Parser.parser import Parser
from CeylonInterpreter.Semantic.semantic import CeylonSemantic

text = \
'''
for(x = 2; x < 10; x++){

}
'''

parser = Parser()
parser.build()
ast = parser.test(text)

semantic = CeylonSemantic()
semantic.visit(ast)
#printer = ASTPrinter()
#printer.print_node(ast)
