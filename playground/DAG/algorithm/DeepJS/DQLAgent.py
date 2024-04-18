import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.layers import Dense, Dropout
from collections import deque
import random
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2

class DQLAgent:
    def __init__(self, state_size, action_size, gamma, name, layers, model=None):
        self.state_size = state_size
        self.action_size = action_size
        self.layers = layers
        self.memory = deque(maxlen=2000)  # Replay buffer
        self.gamma = gamma  # Discount rate
        self.epsilon = 0.5  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.name = name
        self.update_frequency = 5  # Train the model every 10 timesteps
        self.timestep_since_last_update = 0  # Counter for timesteps since last training
        # self.summary_path = summary_path if summary_path is not None else './tensorboard/%s--%s' % (
        #     name, time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()))
        # self.summary_writer = tf.contrib.summary.create_file_writer(self.summary_path)
        # self.brain = brain
        # self.checkpoint = tf.train.Checkpoint(brain=self.brain)
        # self.model_save_path = model_save_path
        if model == None:
            self.model = self._build_model()
        else:
            self.model = model
        
    # def _build_model(self):
    #     """Builds a deep neural network model."""
    #     model = Sequential()
    #     model.add(Dense(24, input_dim=self.state_size, activation='relu'))
    #     model.add(Dense(24, activation='relu'))
    #     model.add(Dense(self.action_size, activation='linear'))
    #     model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
    #     return model
    
    # def _build_model(self):
    #     """Builds a deep neural network model."""
    #     model = Sequential()
    #     model.add(Dense(3, input_dim=self.state_size, activation='relu'))
    #     model.add(Dense(9, activation='relu'))
    #     model.add(Dense(18, activation='relu'))
    #     model.add(Dense(24, activation='relu'))
    #     model.add(Dense(9, activation='relu'))
    #     model.add(Dense(self.action_size, activation='linear'))
    #     model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
    #     return model

    def _build_model(self):
        """Builds a deep neural network model with added regularization."""
        model = Sequential()
        # Input layer
        model.add(Dense(24, input_dim=self.state_size, activation='relu', kernel_regularizer=l2(0.01)))
        # model.add(Dropout(0.2))
        # Hidden layers
        model.add(Dense(48, activation='relu'))
        # model.add(Dropout(0.2))
        model.add(Dense(96, activation='relu'))
        model.add(Dense(48, activation='relu'))
        # , kernel_regularizer=l2(0.01)
        # model.add(Dropout(0.2))
        model.add(Dense(24, activation='relu'))
        # model.add(Dropout(0.2))
        # Output layer
        model.add(Dense(self.action_size, activation='linear'))
        # Compile model
        model.compile(loss=MeanSquaredError(), optimizer=Adam(learning_rate=self.learning_rate))

        return model

    def remember(self, state, action, reward, next_state, done):
        """Stores experiences in the replay buffer."""
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        """Returns action based on a given state, following an epsilon-greedy policy."""
        print("epsilon value is ", self.epsilon)
        act_values = self.model.predict(state)
        print(act_values)
        if np.random.rand() <= self.epsilon:
            print("i selected randomly")
            return random.randrange(self.action_size)
        
        return np.argmax(act_values[0])
    
    def test_act(self, states):
        print("I am testing the given states")
        for state in states:
            current_state = np.array(state, dtype=np.float32)
            current_state = np.expand_dims(current_state, axis=0)  # Add batch dimension
            act_values = self.model.predict(current_state)
            print(act_values)

    def replay(self, batch_size):
        """Trains the model using randomly sampled experiences from the replay buffer."""
        self.timestep_since_last_update += 1
        if self.timestep_since_last_update >= self.update_frequency:
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
            self.timestep_since_last_update = 0

    def save_model(self):
        model_dir = 'DAG/algorithm/DeepJS/agents/%s/all/%s_%s_%s' % \
        (self.layers, self.name, self.state_size, self.action_size)
        if not os.path.isdir(model_dir):
            os.makedirs(model_dir)
        model_path = os.path.join(model_dir, 'model.h5')
        self.model.save(model_path)
        # self.model.save(model_dir)

# Example usage within SimPy environment
# agent = DQLAgent(state_size=12, action_size=21)  # Define appropriate sizes
# During each pause:
#   action = agent.act(current_state)
#   apply_action_to_simulation(action)
#   agent.remember(state, action, reward, next_state, done)
#   if len(agent.memory) > batch_size:
#       agent.replay(batch_size)
