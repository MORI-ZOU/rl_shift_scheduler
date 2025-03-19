from typing import NamedTuple

from .day import Day
from .employee import Employee


class Condition(NamedTuple):
    employee: Employee
    day: Day

    def __str__(self) -> str:
        return f"{self.employee}__{self.day}"