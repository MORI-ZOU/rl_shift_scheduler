from datetime import date
from typing import NamedTuple


class Day(NamedTuple):
    year: int
    month: int
    day: int

    def __str__(self) -> str:
        return f"Day_{self.year:04}/{self.month:02}/{self.day:02}"

    @classmethod
    def get_instances(cls) -> list["Day"]:
        return [cls(year=2024, month=4, day=d) for d in range(1, 15)]

    @classmethod
    def get_n_instances(cls) -> int:
        return len(cls.get_instances())

    @classmethod
    def from_idx(cls, idx: int) -> "Day":
        instances = cls.get_instances()
        try:
            return instances[idx]
        except:
            raise ValueError(f"Invalid idx: {idx}. Valid idx: 0 <= idx < {len(cls.get_instances())}")

    @classmethod
    def init(cls, year: int, month: int, day: int) -> "Day":
        ins = cls(year=year, month=month, day=day)
        if ins not in cls.get_instances():
            raise ValueError(f"Invalid day: {ins}. Valid ids are {cls.get_instances()}")
        return ins

    @property
    def idx(self) -> int:
        instances = self.get_instances()
        return instances.index(self)

    def to_date(self) -> date:
        return date(year=self.year, month=self.month, day=self.day)

    @property
    def dow_id(self) -> int:
        return self.to_date().weekday()

    @property
    def dow_label(self) -> str:
        # dow_names = ["Mon", "Tue", "Wen", "Thu", "Fri", "Sat", "Sun"]
        dow_names = ["月", "火", "水", "木", "金", "土", "日"]
        return dow_names[self.dow_id]

    @property
    def is_final_day(self) -> bool:
        instances = self.get_instances()
        return self == instances[-1]

    @property
    def is_weekend(self) -> bool:
        return self.dow_id in {5, 6}
