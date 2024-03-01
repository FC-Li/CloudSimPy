import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from collections import deque
import random

class DQLAgent:
    def __init__(self, state_size, action_size, name, brain, gamma, model_save_path=None,
                 summary_path=None):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)  # Replay buffer
        self.gamma = gamma  # Discount rate
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        # self.summary_path = summary_path if summary_path is not None else './tensorboard/%s--%s' % (
        #     name, time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()))
        # self.summary_writer = tf.contrib.summary.create_file_writer(self.summary_path)
        # self.brain = brain
        # self.checkpoint = tf.train.Checkpoint(brain=self.brain)
        # self.model_save_path = model_save_path
        self.model = self._build_model()
        
    def _build_model(self):
        """Builds a deep neural network model."""
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        """Stores experiences in the replay buffer."""
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        """Returns action based on a given state, following an epsilon-greedy policy."""
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        """Trains the model using randomly sampled experiences from the replay buffer."""
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Example usage within SimPy environment
# agent = DQLAgent(state_size=10, action_size=5)  # Define appropriate sizes
# During each pause:
#   action = agent.act(current_state)
#   apply_action_to_simulation(action)
#   agent.remember(state, action, reward, next_state, done)
#   if len(agent.memory) > batch_size:
#       agent.replay(batch_size)
