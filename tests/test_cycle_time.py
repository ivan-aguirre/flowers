import unittest

from flowers.board import Board
from flowers.person import Person
from flowers.task import Queue, Phase, Role, Task


class HistogramTestCase(unittest.TestCase):

    #TODO finish...
    def test_something(self):
        # Flow
        commited: Queue = Queue("Commited")
        development: Phase = Phase("Development")
        ready_for_tests: Queue = Queue("Ready for tests")
        tests: Phase = Phase("Under tests")
        done: Queue = Queue("Done")

        # Team roles
        dev: Role = Role("Developer", phase=development)
        tester: Role = Role("Tester", phase=tests)

        # Team
        andrea_dev: Person = Person(role=dev)
        ivan_dev: Person = Person(role=dev)
        benedict_tester: Person = Person(role=tester)

        # Board
        board: Board = Board("System Maintenance")
        board.columns(commited, development, ready_for_tests, tests, done)
        board.team(andrea_dev, ivan_dev, benedict_tester)

        board.accept(Task(development, 3, tests, 1))
        board.accept(Task(development, 5, tests, 2))
        board.accept(Task(development, 3, tests, 2))
        board.accept(Task(development, 2, tests, 4))
        board.accept(Task(development, 4, tests, 0))

        # First day
        andrea_dev.effort_available = 3
        ivan_dev.effort_available = 4
        benedict_tester.effort_available = 5

        board.run_day()

        self.assertEqual(5, board.unfinished_tasks)
        self.assertEqual([], board.cycle_times)


        # Second day
        andrea_dev.effort_available = 3
        ivan_dev.effort_available = 4
        benedict_tester.effort_available = 5

        board.run_day()

        self.assertEqual(4, board.unfinished_tasks)


        # Third day
        andrea_dev.effort_available = 6
        ivan_dev.effort_available = 3
        benedict_tester.effort_available = 4

        board.run_day()


if __name__ == '__main__':
    unittest.main()
