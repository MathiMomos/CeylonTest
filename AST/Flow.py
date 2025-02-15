class If:
    def __init__(self, condition, left, right):
        self.left = left
        self.condition = condition
        self.right = right

class While:
    def __init__(self, condition, child):
        self.condition = condition
        self.child = child

class For:
    def __init__(self, init_var, condition, auto, block_node):
        self.init_var = init_var
        self.condition = condition
        self.auto = auto
        self.block_node = block_node