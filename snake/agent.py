import numpy as np
from enviroment_1 import SnakeEnv
from model import Model

env = SnakeEnv()
input = env.observation_space.shape
output = env.action_space.n
print(input)
model = Model(input, output)

episodes = 1000
batch_size = 64

for episode in range(episodes):
    state = env.reset()
    done = False
    score = 0

    while not done:
        action = model.Predict(state)
        next_state, reward, done, info = env.step(action)
        model.remember(state, action, reward, next_state, done)
        state = next_state
        score += reward
        env.render()

    if done:
        print(f"Episode: {episode + 1}/{episodes}, Score: {score}, Epsilon: {model.epsilon:.2}")

    if len(model.memory) > batch_size:
        model.replay(batch_size)

#if episode % 100 == 0:
#    model.save(f"SnakeDQN: {episode}.h5")