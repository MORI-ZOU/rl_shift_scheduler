import gymnasium as gym
from gymnasium import spaces
import numpy as np
from consts import Day, Employee, Shift
from variables import Variables
from extra import show_shift, get_penalties, evalShift


class SchedulerEnv(gym.Env):
    """
    "state": 現在対象となる社員番号、日番号、及びこれまでの割当状況の要約（例：すでに決定済みのシフト数）
    "action_mask": 現在の社員・日に対して選択可能なシフトかどうかを表すバイナリベクトル
    "avail_actions": 固定的に全行動が選択可能かを示す（今回は全て1）

    ・社員数×日数のシフト表を埋めていく。初期値は0(休み)
    """

    metadata = {"render.modes": ["human"]}

    def __init__(self):
        super(SchedulerEnv, self).__init__()

        # 社員・日の定義（従来通り固定のものを利用）
        self.employees = Employee.get_instances()
        self.days = Day.get_instances()
        self.n_employees = len(self.employees)
        self.n_days = len(self.days)
        self.total_steps = self.n_employees * self.n_days

        # 利用するシフト候補（すべてのシフトを候補とする）
        self.shifts = Shift.get_instances()
        self.n_shifts = len(self.shifts)

        # エピソード内に決定するシフト割当（整数リスト：各要素が各ポジションでのシフト idx）
        self.schedule = None

        # 現在のステップ（0～total_steps-1）
        self.current_step = None

        # 状態空間：ここでは Dict 型で返す予定
        # "state" 部分は、例として [current employee index, current day index, 決定済み割当数] の3要素の整数ベクトルとする
        state_low = np.array([0, 0, 0], dtype=np.int32)
        state_high = np.array([self.n_employees - 1, self.n_days - 1, self.total_steps], dtype=np.int32)
        state_space = spaces.Box(low=state_low, high=state_high, shape=(3,), dtype=np.int32)
        action_mask_space = spaces.Box(low=0, high=1, shape=(self.n_shifts,), dtype=np.uint8)
        avail_actions_space = spaces.Box(low=0, high=1, shape=(self.n_shifts,), dtype=np.uint8)

        self.observation_space = spaces.Dict({"state": state_space, "action_mask": action_mask_space, "avail_actions": avail_actions_space})

        # 行動空間：離散値（0～n_shifts-1）
        self.action_space = spaces.Discrete(self.n_shifts)

    def reset(self, seed=None, options=None):
        """
        エピソード開始時の初期化。
        ・割当スケジュールは未決定位置を 0 で初期化
        ・ステップカウンタを0にする
        ・状態（obs）を更新して返す
        """
        self.schedule = [0] * self.total_steps
        self.current_step = 0
        obs = self._get_obs()
        # Gymnasium では (observation, info) のタプルを返すのが仕様
        return obs, {}

    def _get_obs(self):
        """
        現在のステップから状態情報とアクションマスクを生成

        状態情報：
        - 現在対象の社員インデックス、日インデックス
        - 現時点で決定済みのシフト数（単純な進捗指標）

        アクションマスク：
        - 現在対象の社員・日に対し、以下の点で絞り込みを実施
        ① もしその日が「休みの日」であれば、「休」シフト（Shift id "O"）のみを許容
        ② それ以外の場合は、社員が forbidden_shifts, スキルが forbiden_shifts に含むシフトは不可とする
        （※元の個体生成関数 generate_individual の論理を参考）
        - マスクは長さ n_shifts の 0/1 ベクトル
        """
        e_idx = self.current_step // self.n_days
        d_idx = self.current_step % self.n_days
        # 状態情報としてはシンプルに [e_idx, d_idx, 採用済み割当数]
        progress = self.current_step  # すでに決定済みの数
        state_vector = np.array([e_idx, d_idx, progress], dtype=np.int32)

        # 現在対象の社員、日オブジェクト
        current_employee = self.employees[e_idx]
        current_day = self.days[d_idx]

        # アクションマスクの作成
        # まずすべて選択可能とし、その後制約に合わないものを 0 に設定
        mask = np.ones(self.n_shifts, dtype=np.uint8)

        # ① 日の勤務状況に応じた制約：
        # もし current_day が休みの日（work_cycle.check_is_rest_day）なら、通常「休」以外は不可
        if current_employee.work_cycle.check_is_rest_day(current_day):
            for s in self.shifts:
                if s.id != "O":  # 「休」以外は不可
                    mask[s.idx] = 0
        else:
            # ② 社員の個別制約（forbidden_shifts）およびスキルによる制約を反映
            for s in self.shifts:
                if s in current_employee.forbidden_shifts:
                    mask[s.idx] = 0
                if s in current_employee.skill.forbidden_shifts:
                    mask[s.idx] = 0
                # ※シフト "O"（休み）は、休み出ない日には通常選ばせない（個体生成時と同様）のなら除外
                if s.id == "O":
                    mask[s.idx] = 0

        # avail_actions は、常に全アクションが存在するものとする
        avail_actions = np.ones(self.n_shifts, dtype=np.uint8)

        obs = {"state": state_vector, "action_mask": mask, "avail_actions": avail_actions}
        return obs

    def step(self, action):
        """
        現在の(社員, 日)に対して、選択されたシフト(action)を記録。
        もしエピソードが終了した場合は、Variables の評価関数を用いて
        全体のペナルティを求め、報酬 = -（ペナルティ総和）とする。
        """
        # 現在のステップに対して行動を記録
        self.schedule[self.current_step] = action

        self.current_step += 1
        done = self.current_step >= self.total_steps

        # 途中は報酬は 0; エピソード終了時に全体評価
        if not done:
            reward = 0.0
            obs = self._get_obs()

        ## ペナルティ定義
        total_penalty = evalShift(self.schedule)

        reward = -total_penalty  # 目的はペナルティ最小化
        # 最終状態は適当な情報にする（たとえば進捗が終端を示す）
        obs = {
            "state": np.array([self.n_employees - 1, self.n_days - 1, self.total_steps], dtype=np.int32),
            "action_mask": np.zeros(self.n_shifts, dtype=np.uint8),
            "avail_actions": np.zeros(self.n_shifts, dtype=np.uint8),
        }

        info = {"schedule": self.schedule.copy()}
        return obs, reward, done, False, info

    def render(self, mode="human"):
        # スケジュールの各要素がNumPyのarrayなどの場合は、plain intに変換して表示する
        clean_schedule = [int(x) if isinstance(x, (np.ndarray, np.generic)) else x for x in self.schedule]
        if self.current_step >= self.total_steps:
            print("最終スケジュール:")
            # show_shift() にplainなリストを渡す、もしくは自前で整形表示
            show_shift(clean_schedule)
            pena_list = get_penalties(clean_schedule)
            for i, p in enumerate(pena_list):
                print(f"p{i+1}: {p}")
        else:
            print("現在のステップ:", self.current_step)
            show_shift(clean_schedule)

    def close(self):
        pass
