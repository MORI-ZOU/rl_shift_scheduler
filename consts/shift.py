from typing import NamedTuple


class Shift(NamedTuple):
    id: str

    def __str__(self) -> str:
        return f"Shift_id{self.id}"

    @classmethod
    def get_instances(cls) -> list["Shift"]:
        ## O:休み、D:日勤、N:夜勤, S:時差
        return [cls(id=id) for id in ["O", "D", "N", "S"]]

    @classmethod
    def get_n_instances(cls) -> int:
        return len(cls.get_instances())

    @classmethod
    def from_idx(cls, idx: int) -> "Shift":
        instances = cls.get_instances()
        try:
            return instances[idx]
        except:
            raise ValueError(f"Invalid idx: {idx}. Valid idx: 0 <= idx < {len(cls.get_instances())}")

    @classmethod
    def init(cls, id: str) -> "Shift":
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
            "O": "休",
            "D": "日",
            "N": "夜",
            "S": "時",
        }
        return id_to_label_dict[self.id]

    @property
    def min_worker(self) -> int:
        id_to_label_dict = {
            "O": 1,
            "D": 1,
            "N": 1,
            "S": 1,
        }
        return id_to_label_dict[self.id]

    @property
    def max_worker(self) -> int:
        id_to_label_dict = {
            "O": 2,
            "D": 2,
            "N": 2,
            "S": 2,
        }
        return id_to_label_dict[self.id]

    @classmethod
    def get_forbidden_transitions(cls) -> list[tuple["Shift", "Shift"]]:
        return [
            # previous shift -> current shift
            (cls.init(id="N"), cls.init(id="N")),
            (cls.init(id="N"), cls.init(id="S")),
            (cls.init(id="S"), cls.init(id="N")),
        ]
