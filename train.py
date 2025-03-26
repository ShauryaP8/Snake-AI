#train.py
from snake_env import SnakeGame
from dqn_agent import DQNAgent
import numpy as np

EPISODES = 1000
BATCH_SIZE = 32

env = SnakeGame()
state_size = 7 # From _get_state()
action_size = 3 # 0=straight 1=left, 2=right
agent = DQNAgent(state_size, action_size)

for episode in range(EPISODES):
    state = env.reset()
    state = np.reshape(state, [1, state_size])
    total_reward = 0
    done = False
    while not done:
        action = agent.act(state)
        next_state, reward, done = env.step(action)
        next_state = np.reshape(next_state, [1, state_size])
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward

        if done:
            print(f"Episode {episode+1}/{EPISODES}, Score: {env.score}, Epsilon: {agent.epsilon:.2f}")
            break

        if len(agent.memory) > BATCH_SIZE:
            agent.replay(BATCH_SIZE)

    if (episode+1) % 100 == 0:
        agent.model.save(f'snake_dqn_{episode+1}.h5')
