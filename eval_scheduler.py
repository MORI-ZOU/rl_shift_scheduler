from stable_baselines3 import PPO
from scheduling.old.scheduling_env import SchedulerEnv

env = SchedulerEnv()

model = PPO.load("logs/best_model.zip", env, verbose=1)

obs = env.reset()
done = False
total_reward = 0
while not done:
    action, _ = model.predict(obs)
    obs, reward, done, info = env.step(action)
    total_reward += reward
    print("Total reward:", total_reward)

env.render()
