from CeylonInterpreter.Parser.parser import Parser
from CeylonInterpreter.Semantic.semantic import CeylonSemantic
from CeylonInterpreter.Interpreter.interpreter import Interpreter

text = \
    '''
        print("Hola, como te llamas?");
        scan(saludo);
        print("Hola " ... saludo ... ", cual es tu edad?");
        
        scan(edad);
        print("Tienes " ... edad ... " años");
        
        edad = tonum(edad) + 1;
        # Hola
        print("El proximo año tendras " ... tostr(edad) ... " años");
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
