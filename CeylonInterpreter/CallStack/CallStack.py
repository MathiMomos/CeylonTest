class CallStack:
    def __init__(self):
        self.records = []

    def push(self, ar):
        self.records.append(ar)

    def pop(self):
        return self.records.pop()

    def peek(self):
        return self.records[-1]