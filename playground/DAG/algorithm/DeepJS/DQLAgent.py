import numpy as np
import os
import pickle
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.layers import Dense, Dropout
from collections import deque
import random
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
from keras.models import clone_model

class DQLAgent:
    def __init__(self, state_size, action_size, gamma, name, layers, model=None):
        self.state_size = state_size
        self.action_size = action_size
        self.layers = layers
        self.memory = deque(maxlen=2000)  # Replay buffer
        self.gamma = gamma  # Discount rate
        self.epsilon = 0.7  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.learning_rate_decay = 0.9
        self.decay_steps = 2
        self.global_step = 0
        self.name = name
        self.update_frequency = 4  # Train the model every 10 timesteps
        self.target_update_frequency = 20
        self.timesteps_since_last_target_update = 0  # Counter for timesteps since last training
        self.timesteps_since_last_update = 0
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
        self.target_model = clone_model(self.model)
        self.target_model.set_weights(self.model.get_weights())  # Initialize target network with same weights
        
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
        model.add(Dense(96, activation='relu', kernel_regularizer=l2(0.01)))
        # model.add(Dropout(0.2))
        model.add(Dense(192, activation='relu', kernel_regularizer=l2(0.01)))
        model.add(Dense(96, activation='relu', kernel_regularizer=l2(0.01)))
        # , kernel_regularizer=l2(0.01)
        # model.add(Dropout(0.2))
        model.add(Dense(24, activation='relu', kernel_regularizer=l2(0.01)))
        # model.add(Dropout(0.2))
        # Output layer
        model.add(Dense(self.action_size, activation='linear'))
        # Compile model
        model.compile(loss=MeanSquaredError(), optimizer=Adam(learning_rate=self.learning_rate))

        return model

    def remember(self, state, action, reward, next_state, done):
        """Stores experiences in the replay buffer."""
        self.memory.append((state, action, reward, next_state, done))
    
    # def custom_loss(self):
    #     error = self.action_scores - self.target_values
    #     abs_loss = tf.abs(error)
    #     square_loss = 0.5 * tf.pow(error, 2)
    #     self.huber_loss = tf.where(abs_loss <= self.huber_loss_threshold,
    #                             square_loss,
    #                             self.huber_loss_threshold * (abs_loss - 0.5 * self.huber_loss_threshold))

    def act(self, state):
        """Returns action based on a given state, following an epsilon-greedy policy."""
        print("epsilon value is ", self.epsilon)
        act_values = self.model.predict(state)
        print("the q values are", act_values)    
        print("the target network values are", self.target_model.predict(state))
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
        self.timesteps_since_last_update += 1
        self.timesteps_since_last_target_update += 1
        self.update_frequency = 0
        if self.timesteps_since_last_update >= self.update_frequency:
            minibatch = random.sample(self.memory, batch_size)
            # minibatch = self.memory
            for state, action, reward, next_state, done in minibatch:
                # self.global_step += 1
                # current_learning_rate = self.decay_learning_rate(self.learning_rate, self.global_step, self.decay_steps, self.learning_rate_decay)
                target = reward
                if not done:
                    # target = target_f[0][action] + self.learning_rate * \
                    # (reward + self.gamma * np.amax(self.model.predict(next_state)[0]) - target_f[0][action])
                    target = reward + self.gamma * np.amax(self.target_model.predict(next_state)[0])
                target_f = self.model.predict(state)
                print(target_f)
                print(f"the action selected is {action} with before value {target_f[0][action]}"\
                f"and new value {target}")
                target_f[0][action] = target
                print("the q network values before training are", self.model.predict(state))
                self.model.fit(state, target_f, epochs=1, verbose=1)
                print("the q network values after training are", self.model.predict(state))
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay
            self.timestep_since_last_update = 0
        if self.timesteps_since_last_target_update >= self.target_update_frequency:
            print("Here is the difference between the target network before and after")
            print(self.target_model.predict(state))
            print(np.amax(self.target_model.predict(state)[0]))
            self.target_model = clone_model(self.model)
            self.target_model.set_weights(self.model.get_weights()) 
            print(self.target_model.predict(state))
            self.timesteps_since_last_target_update = 0
    
    def decay_learning_rate(self, initial_learning_rate, global_step, decay_steps, decay_rate):
        current_learning_rate = initial_learning_rate * (decay_rate ** (global_step // decay_steps))
        return current_learning_rate
    
    def save_episode(self):
        # Create directory for episodes if it doesn't exist
        episodes_dir = 'DAG/algorithm/DeepJS/episodes'
        if not os.path.exists(episodes_dir):
            os.makedirs(episodes_dir) 
        # Find the first available episode number
        episode_num = 1
        while os.path.exists(os.path.join(episodes_dir, f'episode_{episode_num}.pkl')):
            episode_num += 1
        # Save replay buffer to file
        episode_filename = f'episode_{episode_num}.pkl'
        episode_path = os.path.join(episodes_dir, episode_filename)
        with open(episode_path, 'wb') as f:
            pickle.dump(self.memory, f)

    def save_model(self):
        model_dir = 'DAG/algorithm/DeepJS/agents/%s/all/%s_%s_%s' % \
        (self.layers, self.name, self.state_size, self.action_size)
        print(model_dir)
        self.save_episode()
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
