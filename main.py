from CeylonInterpreter.Parser.parser import Parser
from CeylonInterpreter.Semantic.semantic import CeylonSemantic
from CeylonInterpreter.Interpreter.interpreter import Interpreter


text = \
'''
x = 5;

switch (x) {
    case 5 {
        print("x es 5");
    }
    case 10 {
        print("x es 10");
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
