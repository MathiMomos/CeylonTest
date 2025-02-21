class NoOp:
    pass

class Print:
    def __init__(self, child):
        self.child = child

class Scan:
    def __init__(self ,type, child):
        self.type = type
        self.child = child
