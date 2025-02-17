from CeylonInterpreter.Parser.parser import Parser
from CeylonInterpreter.Semantic.semantic import CeylonSemantic

text = \
'''
final x = 5;
final y = 6;
z = 7;

for (asd = 5; x < 10; asd++) {

}

while(y == 6){
    z+=1;
}
if (true) {
    valorCondicional = true;
}

fn Sum(x, y) {
    fg = null;
}

'''
parser = Parser()
parser.build()
ast = parser.test(text)

semantic = CeylonSemantic()
semantic.visit(ast)
#printer = ASTPrinter()
#printer.print_node(ast)
