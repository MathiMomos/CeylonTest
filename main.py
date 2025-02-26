from CeylonInterpreter.Parser.parser import Parser
from CeylonInterpreter.Semantic.semantic import CeylonSemantic
from CeylonInterpreter.Interpreter.interpreter import Interpreter

file_name = 'example.cey'

with open('Scripts/' + file_name, 'r') as file:
    text = file.read()

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