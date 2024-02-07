import tensorflow as tf, numpy as np, random
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense
from keras.activations import relu as relu
from keras.optimizers import Adam as optimizer
from keras.losses import MeanSquaredError as loss
from collections import deque


class Model():
    def __init__(self, input, output):
        self.state_input = input
        self.action_output = output
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate = 0.001
        self.model = self.ModelArchitecture()

    def ModelArchitecture(self):
        model = Sequential()
        model.add(Conv2D(16, (4, 4), strides=(2,2), activation=relu, input_shape=(self.state_input)))
        model.add(Flatten())
        model.add(Dense(24, activation=relu))
        model.add(Dense(self.action_output))
        model.compile(loss=loss(), optimizer=optimizer())
        print(model.summary())
        return model
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def Predict(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_output)
        predict_values = self.model.predict(state)
        return np.argmax(predict_values[0])
    
    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.max(self.model.predict(next_state)))
            target_f = self.model.predict(state)
            target_f = [0] * 4
            target_f[action] = target
            state = np.reshape(state, (640, 480, 1))
            target_f =  np.array([target_f])
            state = np.array([state])
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            print(self.epsilon)
        






