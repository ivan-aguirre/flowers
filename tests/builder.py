from flowers.person import Person
from tests.test_board import Role, Phase

development: Phase = Phase("Development")


def build_developer():
    r: Role = Role("developer", phase=development)
    return Person(role=r)
