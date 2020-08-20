from unittest import TestCase

from flowers.person import Person
from flowers.task import Task, OtherPhaseException
from tests import builder
from tests.builder import build_developer




class TestTask(TestCase):

    def test_task_completed(self):
        p: Person = build_developer()
        p.effort_available = 10
        self.assertEqual(p.effort_available, 10)

        t: Task = Task(p.role.phase, 10)
        self.assertEqual(t.current_effort, 10)

        t.apply_effort_from(p)

        self.assertEqual(t.current_effort, 0)
        self.assertEqual(p.effort_available, 0)

    def test_task_half_completed(self):
        p: Person = build_developer()
        p.effort_available = 3
        self.assertEqual(p.effort_available, 3)

        t: Task = Task(p.role.phase, 10)
        self.assertEqual(t.current_effort, 10)

        t.apply_effort_from(p)

        self.assertEqual(t.current_effort, 7)
        self.assertEqual(p.effort_available, 0)

    def test_two_tasks_one_completed(self):
        p: Person = build_developer()
        p.effort_available = 15
        self.assertEqual(p.effort_available, 15)

        t1: Task = Task(p.role.phase, 10)
        t1.apply_effort_from(p)
        self.assertEqual(t1.current_effort, 0)
        self.assertEqual(p.effort_available, 5)

        t2: Task = Task(p.role.phase, 10)
        self.assertEqual(t2.current_effort, 10)
        t2.apply_effort_from(p)

        self.assertEqual(t2.current_effort, 5)
        self.assertEqual(p.effort_available, 0)

    def test_person_exhausted(self):
        p: Person = build_developer()
        p.effort_available = 10
        self.assertEqual(p.effort_available, 10)

        t1: Task = Task(p.role.phase, 10)
        t1.apply_effort_from(p)
        self.assertEqual(t1.current_effort, 0)
        self.assertEqual(p.effort_available, 0)

        t2: Task = Task(p.role.phase, 1)
        self.assertEqual(t2.current_effort, 1)
        t2.apply_effort_from(p)

        # nothing changes...
        self.assertEqual(t2.current_effort, 1)
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
        self.assertEqual(t.current_effort, 10)
        self.assertEqual(p1.effort_available, 0)

        t.apply_effort_from(p2)
        self.assertEqual(3, t.current_effort)
        self.assertEqual(0, p1.effort_available)

    def test_effort_on_different_phase(self):
        p1: Person = build_developer()

        t: Task = Task(builder.Test_phase, 0)
        self.assertRaises(OtherPhaseException, lambda: t.apply_effort_from(p1))
