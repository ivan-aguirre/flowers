from flowers.person import Person


class OtherPhaseException(BaseException):
    pass


class Queue(object):
    def __init__(self, name):
        self.name = name


class Phase(object):
    def __init__(self, name):
        self.name = name


class Role(object):
    def __init__(self, name: str, phase: Phase):
        self.name = name
        self.phase = phase
        pass


class Task(object):
    def __init__(self, *effort_map):
        self.cycle_time = None
        if len(effort_map) % 2 != 0:
            raise Exception('EffortMap requires (Phases, Effort) pairs')
        it = iter(effort_map)
        self.effort_dict = dict(zip(it, it))
        self.current_phase, self.current_effort = self._next_phase()
        self.ready = False

    def _next_phase(self):
        return next(((phase, effort) for (phase, effort) in self.effort_dict.items() if effort > 0), (None, 0))

    def apply_effort_from(self, p: Person):
        if self.current_phase != p.role.phase:
            raise OtherPhaseException()

        required = self.current_effort
        required -= p.consume_effort(required)
        self.effort_dict[p.role.phase] = required

        if required == 0:
            self.current_phase, self.current_effort = self._next_phase()
        else:
            self.current_effort = required

        if self.current_effort == 0:
            self.ready = True

    def effort_required_for(self, phase: Phase):
        return self.effort_dict[phase]

