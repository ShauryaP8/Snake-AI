from snake_env import SnakeGame
from dqn_agent import DQNAgent
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model('snake_dqn_1000.h5') #Load best model
env = SnakeGame()
state = env.reset()
state = np.reshape(state, [1,7])
done = False

while not done:
    action = np.argmax(model.predict(state, verbose=0)[0])
    next_state, reward, done = env.step(action)
    env.render() #Watch it play
    state = np.reshape(next_state, [1,7])
    if done:
        print(f"Final Score: {env.score}")
        break

