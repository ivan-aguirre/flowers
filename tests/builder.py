from flowers.person import Person
from tests.test_board import Role, Phase

Development_phase: Phase = Phase("Development")
Test_phase: Phase = Phase("Test")


def build_developer():
    r: Role = Role("developer", phase=Development_phase)
    return Person(role=r)
