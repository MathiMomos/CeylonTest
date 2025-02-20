from CeylonInterpreter.Parser.parser import Parser
from CeylonInterpreter.Semantic.semantic import CeylonSemantic
from CeylonInterpreter.Interpreter.interpreter import Interpreter


text = \
'''
fn factorial(n) {
    if (n == 0) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

x = factorial(6);
print(x);
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
