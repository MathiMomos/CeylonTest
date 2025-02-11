from lexer import CeylonLexer
from parser import Parser
import AST

text = \
'''

fn suma(a, b) {
    resultado = a + b;
}

fn verificarNumero(x) {
    if (x > 0) {
        estado = 1;
    } elif (x < 0) {
        estado = -1;
    } else {
        estado = 0;
    }
}

fn contarHasta(n) {
    sumaTotal = 0;
    i = 1;
    while (i <= n) {
        sumaTotal += i;
        i++;
    }
}
'''

lexer = CeylonLexer()
lexer.build()
parser = Parser(lexer)
parser.build()
ast = parser.test(text)

printer = AST.ASTPrinter()
printer.print_node(ast)