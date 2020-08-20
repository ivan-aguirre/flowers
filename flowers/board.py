
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
        for task in [t for t in self.tasks if not t.ready]:
            if task.cycle_time is None:
                task.cycle_time = 1
            else:
                task.cycle_time += 1

            current_phase = task.current_phase
            for person in [p for p in self._team if p.role.phase == current_phase]:
                if person.role.phase == task.current_phase:
                    task.apply_effort_from(person)
