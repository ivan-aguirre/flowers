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
        self.effort_required_now = next(iter(self.effort_dict.values()))

    def apply_effort_from(self, p: Person):
        required = self.effort_dict[p.role.phase]
        required -= p.consume_effort(required)

        self.effort_dict[p.role.phase] = required
        self.effort_required_now = required

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
        for people in self._team:
            task.apply_effort_from(people)

