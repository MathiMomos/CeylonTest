from enum import Enum

class ART(Enum): # ARType
    PROGRAM = "PROGRAM"
    FUNCTION = "FUNCTION"
    IF = "IF"
    WHILE = "WHILE"
    FOR = "FOR"
    CASE = "CASE"

class AR:
    def __init__(self, name, ar_type, nesting_level, enclosing_ar = None):
        self.name = name
        self.ar_type = ar_type
        self.nesting_level = nesting_level
        self.members = {}
        self.enclosing_ar = enclosing_ar
        self.returning_value = None

    # dictlike
    def __setitem__(self, key, member): # key is member name
        self.members[key] = member

    # dictlike
    def __getitem__(self, key):
        try:
            return self.members[key]
        except KeyError:
            return

    # dedicated method
    def set(self, key, member):
        saved_member = self.get(key)

        if not saved_member: # member is None, creates a new member
            self.members[member.name] = member
            return

        # saved member is a reference to the located member, so the function update it
        saved_member.name = member.name
        saved_member.value = member.value
        saved_member.type = member.type

    # dedicated method
    def get(self, key, origin = True): # key is member name
        saved_member = self[key] # finds in the current AR

        if saved_member is None and self.enclosing_ar is not None:
            saved_member = self.enclosing_ar.get(key, origin = False) # finds in the enclosing AR (Recursive)

        if not origin: # break down if not the origin call
           return saved_member

        if saved_member is None:
            return # returns none

        return saved_member # returns the found member

    def __str__(self):
        lines = [f"AR({self.name}, type={self.ar_type}, nesting_level={self.nesting_level})"]
        lines.append("Members:")
        for key, member in self.members.items():
            lines.append(f"  {key}: {member.value} ({member.member_type.name})")
        return "\n".join(lines)