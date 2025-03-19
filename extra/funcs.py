from variables import Variables
from consts import Employee, Day, Shift
import pandas as pd


# ペナルティ定義部分
def evalShift(individual) -> int:
    vars = Variables(individual)
    # 勤務日に割り当てられた休みをカウント
    c1 = vars.count_assigned_holiday_on_weekdays()

    # 必要なスキルを持っていない人が割り当てられた回数をカウント
    c2 = vars.count_assigned_not_have_required_skill()

    # 休日にシフトが割り当てられている数をカウント
    c3 = vars.count_assinged_shift_on_holiday()

    # 1サイクルで1シフトの制約を無視した回数をカウント
    c4 = vars.count_ignore_cycle()

    # シフトの遷移制限を無視した回数をカウントする
    c5 = vars.count_ignore_shift_transition_constraint()

    # 各シフトの人数制限と割り当てられた人数の差分を取得する
    c6 = vars.count_difference_need_and_actual()

    # 1サイクルで1日以上休みがない人数をカウント
    c7 = vars.count_not_assigned_holiday_on_cycle()

    # return (c1 + c2 + c3 + c4 + 2 * c5 + c6 + c7,)
    return c1 + c4


def get_penalties(individual) -> list[int]:
    vars = Variables(individual)

    pena_list = []
    # 勤務日に割り当てられた休みをカウント
    pena_list.append(vars.count_assigned_holiday_on_weekdays())

    # 必要なスキルを持っていない人が割り当てられた回数をカウント
    pena_list.append(vars.count_assigned_not_have_required_skill())

    # 休日にシフトが割り当てられている数をカウント
    pena_list.append(vars.count_assinged_shift_on_holiday())

    # 1サイクルで1シフトの制約を無視した回数をカウント
    pena_list.append(vars.count_ignore_cycle())

    # シフトの遷移制限を無視した回数をカウントする
    pena_list.append(vars.count_ignore_shift_transition_constraint())

    # 各シフトの人数制限と割り当てられた人数の差分を取得する
    pena_list.append(vars.count_difference_need_and_actual())

    # 1サイクルで1日以上休みがない人数をカウント
    pena_list.append(vars.count_not_assigned_holiday_on_cycle())

    return pena_list


def show_shift(indivisual):
    all_work = []
    index = 0
    for e in range(Employee.get_n_instances()):
        emp_work = []
        for d in range(Day.get_n_instances()):
            emp_work.append(Shift.from_idx(indivisual[index]).label)
            index += 1
        all_work.append(emp_work)

    header = []
    for d in Day.get_instances():
        header.append(f"{d.day}({d.dow_label})")

    names = []
    for e in Employee.get_instances():
        names.append(e.label)

    pd.set_option("display.unicode.east_asian_width", True)
    df_schedule = pd.DataFrame(all_work, columns=header, index=names)
    print(df_schedule)
