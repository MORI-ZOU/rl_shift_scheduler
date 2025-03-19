from typing import NamedTuple

from .day import Day
from .shift import Shift
from .skill import Skill
from .work_cycle import WorkCycle


class Employee(NamedTuple):
    id: str

    def __str__(self) -> str:
        return f"Employee_id{self.id}"

    @classmethod
    def get_instances(cls) -> list["Employee"]:
        return [
            cls(id=id)
            for id in [
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
                "g",
                "h",
                "i",
                # "j",
                # "k",
                # "l",
            ]
        ]

    @classmethod
    def get_n_instances(cls) -> int:
        return len(cls.get_instances())

    @classmethod
    def from_idx(cls, idx: int) -> "Employee":
        instances = cls.get_instances()
        try:
            return instances[idx]
        except:
            raise ValueError(f"Invalid idx: {idx}. Valid idx: 0 <= idx < {len(cls.get_instances())}")

    @classmethod
    def init(cls, id: str) -> "Employee":
        ins = cls(id=id)
        if ins not in cls.get_instances():
            raise ValueError(f"Invalid id: {id}. Valid ids are {cls.get_instances()}")
        return ins

    @property
    def idx(self) -> int:
        instances = self.get_instances()
        return instances.index(self)

    @property
    def label(self) -> str:
        id_to_label_dict = {
            "a": "A",
            "b": "B",
            "c": "C",
            "d": "D",
            "e": "E",
            "f": "F",
            "g": "G",
            "h": "H",
            "i": "I",
            # "j": "J",
            # "k": "K",
            # "l": "L",
        }
        return id_to_label_dict[self.id]

    @property
    def skill(self) -> Skill:
        id_to_label_dict = {
            "a": Skill(a=True, b=True),
            "b": Skill(a=True, b=True),
            "c": Skill(a=True, b=True),
            "d": Skill(a=True, b=True),
            "e": Skill(a=True, b=True),
            "f": Skill(a=True, b=True),
            "g": Skill(a=True, b=True),
            "h": Skill(a=True, b=True),
            "i": Skill(a=True, b=True),
            # "j": Skill(a=False, b=True),
            # "k": Skill(a=False, b=True),
            # "l": Skill(a=False, b=True),
        }
        return id_to_label_dict[self.id]

    @property
    def work_cycle(self) -> WorkCycle:
        work_cycle_dict = {
            "a": WorkCycle(n_work_days=5, cycle_start=Day(year=2024, month=4, day=1)),
            "b": WorkCycle(n_work_days=5, cycle_start=Day(year=2024, month=4, day=1)),
            "c": WorkCycle(n_work_days=5, cycle_start=Day(year=2024, month=4, day=1)),
            "d": WorkCycle(n_work_days=5, cycle_start=Day(year=2024, month=4, day=1)),
            "e": WorkCycle(n_work_days=5, cycle_start=Day(year=2024, month=4, day=1)),
            "f": WorkCycle(n_work_days=5, cycle_start=Day(year=2024, month=4, day=1)),
            "g": WorkCycle(n_work_days=5, cycle_start=Day(year=2024, month=4, day=1)),
            "h": WorkCycle(n_work_days=5, cycle_start=Day(year=2024, month=4, day=1)),
            "i": WorkCycle(n_work_days=5, cycle_start=Day(year=2024, month=4, day=1)),
            # "j": WorkCycle(n_work_days=5, cycle_start=Day(year=2024, month=4, day=1)),
            # "k": WorkCycle(n_work_days=5, cycle_start=Day(year=2024, month=4, day=1)),
            # "l": WorkCycle(n_work_days=5, cycle_start=Day(year=2024, month=4, day=1)),
        }
        return work_cycle_dict[self.id]

    @property
    def forbidden_shifts(self) -> list[Shift]:
        forbidden_shifts_dict = {
            "a": [],
            "b": [],
            "c": [],
            "d": [],
            "e": [],
            "f": [],
            "g": [],
            "h": [],
            "i": [],
            # "i": [Shift.init(id="Mb"), Shift.init(id="Aa"), Shift.init(id="Nb")],
            # "j": [],
            # "k": [],
            # "l": [],
        }
        return forbidden_shifts_dict[self.id]

    @property
    def holidays(self) -> list[Day]:
        holidays_dict = {
            "a": [],
            "b": [],
            "c": [],
            "d": [],
            "e": [],
            "f": [],
            "g": [],
            "h": [],
            "i": [],
            # "i": [Day(year=2024, month=4, day=3)],
            # "j": [],
            # "k": [],
            # "l": [],
        }
        return holidays_dict[self.id]

    def check_is_holiday(self, day: Day) -> bool:
        if day in self.holidays:
            return True
        else:
            return False
