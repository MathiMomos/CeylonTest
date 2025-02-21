from CeylonInterpreter.Parser.parser import Parser
from CeylonInterpreter.Semantic.semantic import CeylonSemantic
from CeylonInterpreter.Interpreter.interpreter import Interpreter


text = \
'''
cond = true;

while (cond) {
    print("=== Menú Principal ===");
    print("1. Saludar");
    print("2. Mostrar número favorito");
    print("3. Salir");
    print("Selecciona una opción: ");

    scan(opcion);

    if (opcion == "1") {
        print("¡Hola! ¿Cómo estás?");
    } elif (opcion == "2") {
        print("Mi número favorito es el 7.");
    } elif (opcion == "3") {
        print("Saliendo del programa...");
        cond = false;
    } else {
        print("Opción no válida. Intenta de nuevo.");
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
