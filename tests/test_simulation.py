from unittest import TestCase

from flowers.board import Board, run
from flowers.person import Person
from flowers.task import Task, Role, Queue, Phase


class TestSimulation(TestCase):

    def test_simulation_N_days(self):
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

        self.assertEqual(False, task1.done)

        board.accept(task1)
        board.accept(task2)

        # First day
        andrea_dev.effort_available = 3
        ivan_dev.effort_available = 4
        benedict_tester.effort_available = 5

        run(board, days=5)

        self.assertEqual(5, board.days)
        #TODO: After any day, or at the end of the simulation, we must able to query...

    def test_simulation_until_there_s_no_more_tasks(self):
        #TODO: finish
        pass
