from CeylonInterpreter.Parser.parser import Parser
from CeylonInterpreter.Semantic.semantic import CeylonSemantic
from CeylonInterpreter.Interpreter.interpreter import Interpreter

text = \
    '''
        fn suma (a, b) {
            var = 1;
            print(a);
            print(b);
            switch (var) {
                case 1 {
                    c = a + b;
                    print(c);
                }
            }
        }
        
        suma(1, 2);
    '''

# el peak de la programacion

parser = Parser()
parser.build()
ast = parser.test(text)

semantic = CeylonSemantic()
semantic.visit(ast)

interpreter = Interpreter()
interpreter.visit(ast)
# printer = ASTPrinter()
# printer.print_node(ast)
