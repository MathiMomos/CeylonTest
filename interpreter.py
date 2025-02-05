from lexer import Lexer
from parser import Parser

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))
    
class Interpreter(NodeVisitor):
    
    def visit_BinOp(self, node):
        if node.op == "+":
            return self.visit(node.left) + self.visit(node.right)
        elif node.op == "-":
            return self.visit(node.left) - self.visit(node.right)
        elif node.op == "*":
            return self.visit(node.left) * self.visit(node.right)
        elif node.op == "//":
            return self.visit(node.left) // self.visit(node.right)
        elif node.op == "/":
            return float(self.visit(node.left)) / float(self.visit(node.right))
    def visit_Number(self, node):
        return node.value
        
    def visit_UnaryOp(self, node):
        op = node.op
        if op == "+":
            return +self.visit(node.expr)
        elif op == "-":
            return -self.visit(node.expr)
    
lexer = Lexer()
lexer.build()
parser = Parser(lexer)
parser.build()


inter = Interpreter()
res = inter.visit(parser.test("2 + 3 * 4 + 3"))

print(res)