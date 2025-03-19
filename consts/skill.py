from typing import NamedTuple

from .shift import Shift


class Skill(NamedTuple):
    a: bool
    b: bool

    @property
    def forbidden_shifts(self) -> list[Shift]:
        forbidden_shifts_ = []
        if not self.a:
            forbidden_shifts_ += [Shift.init(id="S")]
        if not self.b:
            forbidden_shifts_ += [Shift.init(id="N")]
        return forbidden_shifts_
