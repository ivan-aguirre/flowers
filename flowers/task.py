from flowers.person import Person


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
        if len(effort_map) % 2 != 0:
            raise Exception('EffortMap requires (Phases, Effort) pairs')
        it = iter(effort_map)
        self.effort_dict = dict(zip(it, it))

        self.current_phase, self.current_effort = self._next_phase()

    def _next_phase(self):
        return next(((phase, effort) for (phase, effort) in self.effort_dict.items() if effort > 0), (None, 0))

    def apply_effort_from(self, p: Person):
        required = self.current_effort
        required -= p.consume_effort(required)
        self.effort_dict[p.role.phase] = required

        if required == 0:
            self.current_phase, self.current_effort = self._next_phase()
        else:
            self.current_effort = required

    def effort_required_for(self, phase: Phase):
        return self.effort_dict[phase]


class Board(object):
    def __init__(self, name: str):
        self.name = name
        self.tasks = []
        self._team = None

    def columns(self, *args):
        pass

    def team(self, *team):
        self._team = list(team)

    def accept(self, task):
        self.tasks.append(task)

    def run_day(self):
        task = self.tasks[0]
        for person in self._team:
            if task.current_phase == person.role.phase:
                task.apply_effort_from(person)
