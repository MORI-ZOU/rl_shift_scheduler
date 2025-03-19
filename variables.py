import random
from consts import Condition, Day, Employee, Shift


class Variables:
    def __init__(self, indivisual_list: list[int] = None):
        if indivisual_list is None:
            self.ind_list = self.get_random_list()
        else:
            self.ind_list = indivisual_list

        index = 0
        self._shift_idx_var_dict: dict[Condition, Shift] = {}
        for e in Employee.get_instances():
            for d in Day.get_instances():
                c = Condition(employee=e, day=d)
                self._shift_idx_var_dict[c] = Shift.from_idx(indivisual_list[index])
                index += 1

    def set_random_list(self) -> list[int]:
        ind_random = []
        shift_list = Shift.get_instances()

        for e in Employee.get_instances():
            for d in Day.get_instances():
                shift = random.choice(shift_list)
                ind_random.append(shift.idx)

        return ind_random

    # ある日にある従業員に割り当てられたシフトを取得する
    def get_appshift(self, condition: Condition) -> Shift:
        return self._shift_idx_var_dict[condition]

    @classmethod
    def init_indivisual(cls, icls, content):
        return icls(content)

    @classmethod
    def initPopulation(cls, pcls, ind_init, file):
        return pcls(ind_init(c) for c in file)

    # indivisual初期値
    @classmethod
    def generate_individual(cls) -> list[int]:
        individual = []
        forbidden_trans = Shift.get_forbidden_transitions()

        for e in Employee.get_instances():
            # NGシフトでないかつ休みでないシフトを選ぶ
            ok_shift = []
            for s in Shift.get_instances():
                if s in e.forbidden_shifts:
                    continue
                if s in e.skill.forbidden_shifts:
                    continue
                if s == Shift.init("O"):
                    continue
                ok_shift.append(s)

            if not ok_shift:
                raise Exception(f"利用可能なシフトがありません：{e}")

            app_shift = random.choice(ok_shift)
            for d in Day.get_instances():
                if e.work_cycle.check_is_cycle_end(current_day=d, pattern="rest_to_rest"):
                    # シフト遷移NGでないものの中から次のシフトを選ぶ
                    forbidden_shifts = [pair[1] for pair in forbidden_trans if pair[0] == app_shift]
                    app_ok_shift = [shift for shift in ok_shift if shift not in forbidden_shifts]
                    app_shift = random.choice(app_ok_shift)

                if e.work_cycle.check_is_rest_day(d):
                    # 休みの日は休もう
                    individual.append(Shift.init(id="O").idx)
                    continue

                individual.append(app_shift.idx)
        return individual

    """or-toolsと同じ制約を下記で定義"""

    def count_assigned_holiday_on_weekdays(self):
        # 勤務日に割り当てられた休みをカウント(本当は割り当ててほしくない)
        count = 0
        for e in Employee.get_instances():
            for d in Day.get_instances():
                c = Condition(employee=e, day=d)
                if e.work_cycle.check_is_work_day(current_day=d):
                    if self.get_appshift(c) == Shift.init(id="O"):
                        count += 1
        return count

    def count_assigned_not_have_required_skill(self):
        # 必要なスキルを持っていない人が割り当てられた回数をカウント(本当は割り当ててほしくない)
        count = 0
        for e in Employee.get_instances():
            for d in Day.get_instances():
                c = Condition(employee=e, day=d)
                if not e.work_cycle.check_is_work_day(current_day=d):
                    continue

                for s_forbidden in e.skill.forbidden_shifts:
                    if self.get_appshift(c) == s_forbidden:
                        count += 1
        return count

    def count_assinged_shift_on_holiday(self):
        # 休日にシフトが割り当てられている数をカウント
        count = 0
        for e in Employee.get_instances():
            for d in Day.get_instances():
                c = Condition(employee=e, day=d)
                # if not e.work_cycle.check_is_cycle_end(current_day=d):
                if not e.work_cycle.check_is_rest_day(current_day=d):
                    continue

                if self.get_appshift(c) != Shift.init(id="O"):
                    count += 1
        return count

    def count_ignore_cycle(self):
        # 1サイクルで1シフトの制約を無視した回数をカウント
        count = 0
        for e in Employee.get_instances():
            shifts_in_cycle = set()
            for d in Day.get_instances():
                c = Condition(employee=e, day=d)
                shifts_in_cycle.add(self.get_appshift(c).idx)

                if not (e.work_cycle.check_is_cycle_end(current_day=d, pattern="rest_to_rest") or d.is_final_day):
                    continue

                if len(shifts_in_cycle) > 1:
                    min_value = min(shifts_in_cycle)
                    count += len(shifts_in_cycle) * min_value

                shifts_in_cycle.clear()
        return count

    def count_ignore_shift_transition_constraint(self):
        # シフトの遷移制限を無視した回数をカウントする(先週のシフトと今週のシフトが遷移NGの場合、カウント＋)
        count = 0
        for e in Employee.get_instances():
            shift_in_cycle = []
            shift_in_cycle_prev = []
            for d in Day.get_instances():
                c = Condition(employee=e, day=d)
                day_shift = self.get_appshift(c)
                if day_shift == Shift.init(id="O"):
                    continue
                shift_in_cycle.append(day_shift)

                if not (e.work_cycle.check_is_cycle_end(current_day=d, pattern="rest_to_rest") or d.is_final_day):
                    continue

                if not shift_in_cycle_prev:
                    # 前回シフトが空なら更新だけする
                    shift_in_cycle_prev = shift_in_cycle
                    shift_in_cycle.clear()
                    continue

                for s_previous, s_currenct in Shift.get_forbidden_transitions():
                    if shift_in_cycle_prev.count(s_previous) > 0 and shift_in_cycle.count(s_currenct) > 0:
                        count += shift_in_cycle.count(s_currenct)

                # 前回シフトを更新する
                shift_in_cycle_prev = shift_in_cycle
                shift_in_cycle.clear()
        return count

    def count_difference_need_and_actual(self):
        # 各シフトの人数制限と割り当てられた人数の差分を取得する
        result = []

        for d in Day.get_instances():
            if d.is_weekend:
                continue

            for s in Shift.get_instances():
                if s == Shift.init(id="O"):
                    continue

                warker = 0
                for e in Employee.get_instances():
                    c = Condition(employee=e, day=d)
                    if self.get_appshift(c) == s:
                        warker += 1

                # 割り当てられた従業員数がmaxとminの間に入っていなければペナルティ
                penalty = 0
                min_warker = s.min_worker
                max_warker = s.max_worker

                if warker < min_warker:
                    penalty = min_warker - warker
                elif warker > max_warker:
                    penalty = warker - max_warker

                result.append(penalty)

        return sum(result)

    def count_not_assigned_holiday_on_cycle(self):
        # 1サイクルで1日以上休みがない人数をカウント
        count = 0
        for e in Employee.get_instances():
            shift_in_cycle = []
            for d in Day.get_instances():
                c = Condition(employee=e, day=d)
                shift_in_cycle.append(self.get_appshift(c))

                if not e.work_cycle.check_is_cycle_end(current_day=d, pattern="work_to_rest"):
                    continue

                if shift_in_cycle.count(Shift.init(id="O")) < 1:
                    count += 1

                shift_in_cycle.clear()
        return count
