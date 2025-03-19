from typing import NamedTuple, Literal

from .day import Day


class WorkCycle(NamedTuple):
    """
    労働日と休日のサイクルを管理するクラス

    Attributes:
        n_work_days (int): 労働日数
        cycle_start (Day): サイクルの開始日
    """

    n_work_days: int
    cycle_start: Day

    @property
    def n_rest_days(self) -> int:
        """
        サイクル内の休日数を返します（常に2日）
        """
        return 2

    @property
    def n_cycle_days(self) -> int:
        """
        サイクルの総日数を返します（労働日数 + 休日数）
        """
        return self.n_work_days + self.n_rest_days

    def check_day_in_cycle(self, current_day: Day) -> int:
        """
        指定された日がサイクルの開始から何日目にあたるかを計算します

        Args:
            current_day (Day): 指定日

        Returns:
            int: サイクル開始からの日数
        """
        start_date = self.cycle_start.to_date()
        current_date = current_day.to_date()
        days_since_start = (current_date - start_date).days
        return days_since_start % self.n_cycle_days

    def check_is_rest_day(self, current_day: Day) -> bool:
        """
        指定された日が休日かどうかを判断します

        Args:
            current_day (Day): 指定日

        Returns:
            bool: 指定日が休日であればTrue、そうでなければFalse
        """
        day_in_cycle = self.check_day_in_cycle(current_day=current_day)
        return day_in_cycle >= self.n_work_days

    def check_is_work_day(self, current_day: Day) -> bool:
        """
        指定された日が労働日かどうかを判断します

        Args:
            current_day (Day): 指定日

        Returns:
            bool: 指定日が労働日であればTrue、そうでなければFalse
        """
        day_in_cycle = self.check_day_in_cycle(current_day=current_day)
        return day_in_cycle < self.n_work_days

    def check_is_cycle_end(self, current_day: Day, pattern: Literal["work_to_rest", "rest_to_rest"]) -> bool:
        """
        指定された日がサイクルの最終日かどうかを判断します
        休->休 なら1日目の休みが最終日
        働->休 なら2日目の休みが最終日

        Args:
            current_day (Day): 指定日
            pattern (Literal["work_to_rest", "rest_to_rest"]): サイクルのパターン

        Returns:
            bool: 指定日がサイクル終了日であればTrue、そうでなければFalse
        """
        if pattern == "work_to_rest":
            return self.check_day_in_cycle(current_day=current_day) == self.n_cycle_days - 1
        elif pattern == "rest_to_rest":
            return self.check_day_in_cycle(current_day=current_day) == self.n_cycle_days - 2
        else:
            raise ValueError("'pattern' should be 'work_to_rest' or 'rest_to_rest'.")

