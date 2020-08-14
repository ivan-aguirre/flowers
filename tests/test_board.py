from unittest import TestCase

from flowers.person import Person
from flowers.task import Task, Queue, Phase, Role, Board


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
        tester: Role = Role("Tester", phase=development)

        # Team
        andrea_dev: Person = Person(role=dev)
        ivan_dev: Person = Person(role=dev)
        benedict_tester: Person = Person(role=tester)

        # Board
        board: Board = Board("System Maintenance")
        board.columns(commited, development, ready_for_tests, tests, done)
        board.team(andrea_dev, ivan_dev, benedict_tester)

        task1: Task = Task(development, 10, tests, 20)
        board.accept(task1)

        andrea_dev.effort_available = 7
        ivan_dev.effort_available = 5

        board.run_day()

        self.assertEqual(0, task1.effort_required_for(development))
        self.assertEqual(20, task1.effort_required_for(tests))

        self.assertEqual(0, andrea_dev.effort_available)
        self.assertEqual(2, ivan_dev.effort_available)