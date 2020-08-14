from unittest import TestCase

from flowers.person import Person
from flowers.task import Task, Phase
from tests.builder import build_developer


class TestTask(TestCase):

    def test_task_completed(self):
        p: Person = build_developer()
        p.effort_available = 10
        self.assertEqual(p.effort_available, 10)

        t: Task = Task(p.role.phase, 10)
        self.assertEqual(t.effort_required_now, 10)

        t.apply_effort_from(p)

        self.assertEqual(t.effort_required_now, 0)
        self.assertEqual(p.effort_available, 0)

    def test_task_half_completed(self):
        p: Person = build_developer()
        p.effort_available = 3
        self.assertEqual(p.effort_available, 3)

        t: Task = Task(p.role.phase, 10)
        self.assertEqual(t.effort_required_now, 10)

        t.apply_effort_from(p)

        self.assertEqual(t.effort_required_now, 7)
        self.assertEqual(p.effort_available, 0)

    def test_two_tasks_one_completed(self):
        p: Person = build_developer()
        p.effort_available = 15
        self.assertEqual(p.effort_available, 15)

        t1: Task = Task(p.role.phase, 10)
        t1.apply_effort_from(p)
        self.assertEqual(t1.effort_required_now, 0)
        self.assertEqual(p.effort_available, 5)

        t2: Task = Task(p.role.phase, 10)
        self.assertEqual(t2.effort_required_now, 10)
        t2.apply_effort_from(p)

        self.assertEqual(t2.effort_required_now, 5)
        self.assertEqual(p.effort_available, 0)

    def test_person_exhausted(self):
        p: Person = build_developer()
        p.effort_available = 10
        self.assertEqual(p.effort_available, 10)

        t1: Task = Task(p.role.phase, 10)
        t1.apply_effort_from(p)
        self.assertEqual(t1.effort_required_now, 0)
        self.assertEqual(p.effort_available, 0)

        t2: Task = Task(p.role.phase, 1)
        self.assertEqual(t2.effort_required_now, 1)
        t2.apply_effort_from(p)

        # nothing changes...
        self.assertEqual(t2.effort_required_now, 1)
        self.assertEqual(p.effort_available, 0)

    def test_two_person_one_task(self):
        p1: Person = build_developer()
        p1.effort_available = 10
        self.assertEqual(p1.effort_available, 10)

        p2: Person = build_developer()
        p2.effort_available = 7
        self.assertEqual(p2.effort_available, 7)

        t: Task = Task(p1.role.phase, 20)
        t.apply_effort_from(p1)
        self.assertEqual(t.effort_required_now, 10)
        self.assertEqual(p1.effort_available, 0)

        t.apply_effort_from(p2)
        self.assertEqual(3, t.effort_required_now)
        self.assertEqual(0, p1.effort_available)
