from unittest import TestCase

from flowers.board import Board
from flowers.person import Person
from flowers.task import Queue, Phase, Role, Task


class TestBoardWithMultipleTasks(TestCase):

    def test_two_tasks(self):
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

        task1: Task = Task(development, 3, tests, 1)
        task2: Task = Task(development, 5, tests, 2)

        self.assertEqual(False, task1.ready)

        board.accept(task1)
        board.accept(task2)

        # First day
        andrea_dev.effort_available = 3
        ivan_dev.effort_available = 4
        benedict_tester.effort_available = 5

        board.run_day()
        self.assertEqual(False, task1.ready)
        self.assertEqual(1, task1.cycle_time)
        self.assertEqual(0, task1.effort_required_for(development))
        self.assertEqual(1, task1.effort_required_for(tests))

        self.assertEqual(False, task2.ready)
        self.assertEqual(1, task2.cycle_time)
        self.assertEqual(1, task2.effort_required_for(development))
        self.assertEqual(2, task2.effort_required_for(tests))

        # Second day
        andrea_dev.effort_available = 3
        ivan_dev.effort_available = 4
        benedict_tester.effort_available = 5

        board.run_day()
        self.assertEqual(True, task1.ready)
        self.assertEqual(2, task1.cycle_time)
        self.assertEqual(0, task1.effort_required_for(development))
        self.assertEqual(0, task1.effort_required_for(tests))

        self.assertEqual(False, task2.ready)
        self.assertEqual(2, task2.cycle_time)
        self.assertEqual(0, task2.effort_required_for(development))
        self.assertEqual(2, task2.effort_required_for(tests))

        # Third day
        andrea_dev.effort_available = 6
        ivan_dev.effort_available = 3
        benedict_tester.effort_available = 4

        board.run_day()
        self.assertEqual(True, task1.ready)
        self.assertEqual(2, task1.cycle_time)
        self.assertEqual(0, task1.effort_required_for(development))
        self.assertEqual(0, task1.effort_required_for(tests))

        self.assertEqual(True, task2.ready)
        self.assertEqual(3, task2.cycle_time)
        self.assertEqual(0, task2.effort_required_for(development))
        self.assertEqual(0, task2.effort_required_for(tests))