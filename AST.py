class AST():
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Number(AST):
    def __init__(self, value):
        self.value = value
        
class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class VarAssign(AST):
    def __init__(self, left, op, right):
        self.left = left # Var
        self.op = op # Type of operation
        self.right = right # Expr

class Var(AST):
    def __init__(self, name, type=None):
        self.name = name  # Var name
        self.type = type # Var type


def print_ast(node, indent=0):
    """Imprime el árbol de sintaxis abstracta (AST) de manera legible."""
    # Generar la indentación basada en el nivel de profundidad
    indentation = "  " * indent

    # Si el nodo es una instancia de BinOp
    if isinstance(node, BinOp):
        print(f"{indentation}BinOp: {node.op}")
        print(f"{indentation}  Left:")
        print_ast(node.left, indent + 1)
        print(f"{indentation}  Right:")
        print_ast(node.right, indent + 1)

    # Si el nodo es una instancia de Number
    elif isinstance(node, Number):
        print(f"{indentation}Number: {node.value}")

    # Si el nodo es una instancia de UnaryOp
    elif isinstance(node, UnaryOp):
        print(f"{indentation}UnaryOp: {node.op}")
        print(f"{indentation}  Expression:")
        print_ast(node.expr, indent + 1)

    # Si el nodo es una instancia de VarAssign
    elif isinstance(node, VarAssign):
        print(f"{indentation}VarAssign:")
        print(f"{indentation}  Left (Var): {node.left.name} ({node.left.type if node.left.type else 'None'})")
        print(f"{indentation}  Op: {node.op}")
        print(f"{indentation}  Right:")
        print_ast(node.right, indent + 1)

    # Si el nodo es una instancia de Var
    elif isinstance(node, Var):
        print(f"{indentation}Var: {node.name}, Type: {node.type if node.type else 'None'}")

    # Si el nodo es una instancia de AST (sin tipo específico)
    elif isinstance(node, AST):
        print(f"{indentation}AST (generic)")