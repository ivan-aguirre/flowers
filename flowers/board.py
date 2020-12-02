class Board(object):
    def __init__(self, name: str):
        self.cycle_times = []
        self.unfinished_tasks = 0
        self.name = name
        self.tasks = []
        self._team = None
        self._days = 0

    def columns(self, *args):
        pass

    def team(self, *team):
        self._team = list(team)

    def accept(self, task):
        self.tasks.append(task)
        self.unfinished_tasks += 1

    def run_day(self):
        self._days += 1
        for task in [t for t in self.tasks if not t.done]:
            task.one_more_day()

            current_phase = task.current_phase
            eligible_people = [_person for _person in self._team if _person.can_work_on(current_phase)]
            for person in eligible_people:
                task.apply_effort_from(person)

                if task.done:
                    self.unfinished_tasks -= 1

                if task.current_phase != current_phase:
                    break

    def run(self, days):
        self._days = days

    @property
    def days(self):
        return self._days


def run(board: Board, days: int):
    for _ in range(0, days):
        board.run_day()
