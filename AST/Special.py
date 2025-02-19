class NoOp:
    pass

class Print:
    def __init__(self, child):
        self.child = child