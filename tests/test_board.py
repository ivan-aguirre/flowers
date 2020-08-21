from unittest import TestCase

from flowers.person import Person
from flowers.task import Task, Queue, Phase, Role
from flowers.board import Board


class TestBoard(TestCase):

    def test_board(self):
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

        task1: Task = Task(development, 10, tests, 20)
        self.assertEqual(False, task1.done)

        board.accept(task1)

        # First day
        andrea_dev.effort_available = 3
        ivan_dev.effort_available = 4
        benedict_tester.effort_available = 5

        board.run_day()

        self.assertEqual(False, task1.done)
        self.assertEqual(1, task1.cycle_time)

        self.assertEqual(3, task1.effort_required_for(development))
        self.assertEqual(0, andrea_dev.effort_available)
        self.assertEqual(0, ivan_dev.effort_available)

        self.assertEqual(20, task1.effort_required_for(tests))
        self.assertEqual(5, benedict_tester.effort_available)

        # Second day
        andrea_dev.effort_available = 3
        ivan_dev.effort_available = 4
        benedict_tester.effort_available = 5

        board.run_day()

        self.assertEqual(False, task1.done)
        self.assertEqual(2, task1.cycle_time)

        self.assertEqual(0, task1.effort_required_for(development))
        self.assertEqual(0, andrea_dev.effort_available)
        self.assertEqual(4, ivan_dev.effort_available)

        self.assertEqual(20, task1.effort_required_for(tests))
        self.assertEqual(5, benedict_tester.effort_available)

        # 3th day
        andrea_dev.effort_available = 3
        ivan_dev.effort_available = 4
        benedict_tester.effort_available = 21

        board.run_day()

        self.assertEqual(True, task1.done)
        self.assertEqual(3, task1.cycle_time)

        self.assertEqual(0, task1.effort_required_for(tests))
        self.assertEqual(1, benedict_tester.effort_available)
        self.assertEqual(3, andrea_dev.effort_available)
        self.assertEqual(4, ivan_dev.effort_available)
