class Person(object):
    def __init__(self, role):
        self.effort_available = 0
        self.role = role

    def consume_effort(self, effort_required):
        to_consume = min(effort_required, self.effort_available)
        self.effort_available -= to_consume
        return to_consume
