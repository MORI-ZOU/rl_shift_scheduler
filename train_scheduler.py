from scheduling_env_v2 import SchedulerEnv
from stable_baselines3 import PPO, A2C
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold
from stable_baselines3.common.monitor import Monitor

if __name__ == "__main__":
    # 環境を作成
    env = SchedulerEnv()
    env = Monitor(env, "logs", allow_early_resets=True)

    # 例：エピソードごとに報酬がある閾値に達したら学習終了
    stop_callback = StopTrainingOnRewardThreshold(reward_threshold=0, verbose=1)

    # 学習用の評価環境（学習中のベストモデル保存）
    eval_env = SchedulerEnv()
    eval_callback = EvalCallback(eval_env, best_model_save_path="logs", log_path="logs", callback_on_new_best=stop_callback)

    # エージェント
    model = A2C("MultiInputPolicy", env, verbose=1, device="cuda")

    # 学習
    model.learn(total_timesteps=20000, callback=eval_callback, progress_bar=True)

    model.save("nurse_scheduling/logs/ppo_scheduling.zip")
    print("モデルを ppo_scheduling.zip に保存しました。")

    # 学習終了後，テストエピソードを１回実行して結果表示
    obs, _ = env.reset()
    done = False
    total_reward = 0
    while not done:
        # 学習済み方策から行動決定 (deterministic=True を指定してもよい)
        action, _ = model.predict(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        total_reward += reward
        print("Total reward:", total_reward)

    env.render()
    env.close()
