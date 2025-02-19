from CeylonInterpreter.Parser.parser import Parser
from CeylonInterpreter.Semantic.semantic import CeylonSemantic
from CeylonInterpreter.Interpreter.interpreter import Interpreter

text = \
'''
for (x = 0; x <= 10; x++) {
    if (x % 2 == 0) {
        print(x);
    }
}
'''
parser = Parser()
parser.build()
ast = parser.test(text)

semantic = CeylonSemantic()
semantic.visit(ast)

interpreter = Interpreter()
interpreter.visit(ast)
#printer = ASTPrinter()
#printer.print_node(ast)
