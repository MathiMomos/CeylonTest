class Member:
    def __init__(self, name, value, member_type):
        self.name = name
        self.value = value
        self.member_type = member_type
        self.var_type = None

class BuiltinType:
    def __init__(self, name):
        self.name = name

Number_type = BuiltinType('Number')
String_type = BuiltinType('String')
Boolean_type = BuiltinType('Boolean')
Null_type = BuiltinType('Null')