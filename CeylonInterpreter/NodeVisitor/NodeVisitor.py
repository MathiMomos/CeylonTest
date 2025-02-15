class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + node.__class__.__name__
        method = getattr(self, method_name, self.invalid_node)
        return method(node)

    def invalid_node(self, node):
        raise Exception('Invalid node')