import random
import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import os
import pygame
import random
from code.construction import Road
from code.transformations import TransformCor
from code.vehicle import Vehicle


EPISODES=20000
class Driver:
    def __init__(self, state_size, action_size):
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.state_size = state_size
        self.action_size = action_size
        self.model = self._build_model()

    def load(self, dir_path):
        file_list=self.__sorted_dir(dir_path)
        print('file_list: ',file_list)
        print('Loaded path : ',dir_path+file_list[0])
        self.model.load_weights(dir_path+file_list[0])

    def __sorted_dir(self,folder):
        def getmtime(name):
            path = os.path.join(folder, name)
            return os.path.getmtime(path)

        return sorted(os.listdir(folder), key=getmtime, reverse=True)
    def save(self, name):
        print('Backup ')
        self.model.save_weights(name)
    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:

            return random.randrange(self.action_size)
        act_values = self.model.predict(state)

        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:

            print('------------------')
            if not done:
                print('Not Yet')
                print('reward : ', reward)
                raw_output=self.model.predict(next_state)[0]
                print('raw_output : ', raw_output)
                next_pred=np.amax(raw_output)
                print('next_pred : ',next_pred)
                target = (reward + self.gamma *next_pred)
            else :
                print('Done')
                target = reward
            target_f = self.model.predict(state)
            print('before target_f: ', target_f)
            print(' target: ', target)
            print(' action: ', action)
            target_f[0][action] = target
            print('after : ', target_f)
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

