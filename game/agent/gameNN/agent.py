import numpy as np
import tensorflow as tf
from keras import Sequential
from keras.callbacks import ModelCheckpoint
from keras.layers import Dense
from numpy import unravel_index

import CONSTANT
from game.enviroment.game_env import Game_environment

AGENT_METRIC = 'mae'


class Game_agent:

    def __init__(self):

        self.gamma = 0.85
        self.epsilon = 1.0
        self.epsilon_decay = 0.995

        self.model = self.create_model()
        self.lr_rate = 1e-3

    def get_callbacks(self):
        return [ModelCheckpoint(CONSTANT.DETECTION_ACCURACY_MODEL_PATH,
                                monitor=AGENT_METRIC,
                                verbose=1,
                                save_best_only=True, mode='auto', period=1)]

    def create_model(self):
        # todo: model architecture
        model = Sequential()
        state_shape = self.env.observation_space.shape
        model.add(Dense(24, input_dim=state_shape[0], activation="relu"))
        model.add(Dense(48, activation="relu"))
        model.add(Dense(24, activation="relu"))
        model.add(Dense(self.env.action_space.n))
        model.compile(loss="mse",
                      optimizer=tf.keras.optimizers.Adam(lr=self.lr_rate),
                      metrics=[
                          AGENT_METRIC
                      ])
        return model

    # model = Sequential()
    # model.add(InputLayer(batch_input_shape=(1, 5)))
    # model.add(Dense(10, activation='sigmoid'))
    # model.add(Dense(2, activation='linear'))
    # model.compile(loss='mse', optimizer='adam', metrics=['mae'])

    def reinforcement_learning(self, env: Game_environment, num_episodes=500):
        for i in range(num_episodes):
            s = env.reset()
            self.epsilon *= self.epsilon_decay
            if i % 100 == 0:
                print("Episode {} of {}".format(i + 1, num_episodes))
            done = False
            while not done:
                if np.random.random() < self.epsilon:
                    a = np.random.randint(low=0, high=61, size=(3,))
                else:
                    q_s = self.model.predict(s)
                    a = unravel_index(q_s.argmax(), q_s.shape)
                new_s, r, done, _ = env.step(a)
                target = r + self.gamma * np.max(self.model.predict(new_s))
                target_vec = self.model(s)
                target_vec[a] = target
                self.model.fit(s, np.stack([target_vec], axis=0), epochs=1, verbose=0, callbacks=self.get_callbacks())
                s = new_s
