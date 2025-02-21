from CeylonInterpreter.Parser.parser import Parser
from CeylonInterpreter.Semantic.semantic import CeylonSemantic
from CeylonInterpreter.Interpreter.interpreter import Interpreter


text = \
'''
x = 10;

fn doSomething() {
    fn doInnerSomething() {
        print(x);
    }
    
    doInnerSomething();
}

doSomething();
'''

text2 = \
'''
    x = 0;
    cond = true;
    
    print("Este es tu numero:");
    print(x);
    
    print("Quieres sumarle +5?");
    scanstr(conf);
    
    while(cond) {
        if (conf == "si") {
            x += 5;
            print("Ahora tu numero es:");
            print(x);
            
            print("Quieres sumarle +5?");
            scanstr(conf);
        } else {
            print("Tu numero quedo asi: ");
            print(x);
            cond = false;
        }
    }
'''

# el peak de la programacion

parser = Parser()
parser.build()
ast = parser.test(text)

semantic = CeylonSemantic()
semantic.visit(ast)

interpreter = Interpreter()
interpreter.visit(ast)
#printer = ASTPrinter()
#printer.print_node(ast)
