import os
import pickle
import random
from collections import deque

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class QNetwork(nn.Module):
    def __init__(self, state_size, action_size, layers, activation='ReLU', loss='MSE'):
        super(QNetwork, self).__init__()
        if layers == 5:
            self.fc1 = nn.Linear(state_size, 32)
            self.fc2 = nn.Linear(32, 64)
            self.fc3 = nn.Linear(64, 64)
            self.fc4 = nn.Linear(64, 32)
            self.fc5 = nn.Linear(32, action_size)
        if layers == 6:
            self.fc1 = nn.Linear(state_size, 128)
            self.fc2 = nn.Linear(128, 256)
            self.fc3 = nn.Linear(256, 512)
            self.fc4 = nn.Linear(512, 256)
            self.fc5 = nn.Linear(256, 128)
            self.fc6 = nn.Linear(128, action_size)
        if layers == 7:
            self.fc1 = nn.Linear(state_size, 128)
            self.fc2 = nn.Linear(128, 256)
            self.fc3 = nn.Linear(256, 512)
            self.fc4 = nn.Linear(512,1024)
            self.fc5 = nn.Linear(1024, 256)
            self.fc6 = nn.Linear(256, 128)
            self.fc7 = nn.Linear(128, action_size)

    
        self.activation_func = self.get_activation_function(activation)
        self.loss_func = self.get_loss_function(loss)
    
    def forward(self, x):
        x = self.activation_func(self.fc1(x))
        x = self.activation_func(self.fc2(x))
        x = self.activation_func(self.fc3(x))
        x = self.activation_func(self.fc4(x))
        if hasattr(self, 'fc7'):
            x = self.activation_func(self.fc5(x))
            x = self.activation_func(self.fc6(x))
            x = self.fc7(x)
        else:
            if hasattr(self, 'fc6'):
                x = self.activation_func(self.fc5(x))
                x = self.fc6(x)
            else:
                x = self.fc5(x)
        return x

    def get_activation_function(self, activation):
        if activation == 'ReLU':
            return torch.relu
        elif activation == 'LeakyReLU':
            return nn.LeakyReLU(negative_slope=0.01)
        else:
            raise ValueError("Unknown activation function type: {}".format(activation))

    def get_loss_function(self, loss):
        if loss == 'MSE':
            return nn.MSELoss()
        elif loss == 'Huber':
            return nn.SmoothL1Loss()
        else:
            raise ValueError("Unknown loss function type: {}".format(loss))

class DQLAgent:
    def __init__(self, state_size, action_size, gamma, name, jobs_num, layers, learning_rate, loss, activation, exploration, train_flag=None):
        self.state_size = state_size
        self.action_size = action_size
        self.layers = layers
        self.memory = deque(maxlen=2000)  # Replay buffer
        self.gamma = gamma  # Discount rate
        self.epsilon = exploration  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 1
        self.learning_rate = learning_rate
        self.learning_rate_decay = 0.9
        self.decay_steps = 2
        self.global_step = 0
        self.name = name
        self.jobs_num = jobs_num
        self.loss = loss
        self.activation = activation
        self.update_frequency = 2  # Train the model every 4 timesteps
        self.target_update_frequency = 8
        self.timesteps_since_last_target_update = 0  # Counter for timesteps since last training
        self.timesteps_since_last_update = 0
        self.model = QNetwork(state_size, action_size, layers, activation, loss)
        self.target_model = QNetwork(state_size, action_size, layers, activation, loss)
        self.target_model.load_state_dict(self.model.state_dict())
        self.train_flag = train_flag if train_flag is not None else True

        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.criterion = self.model.loss_func

    def remember(self, state, action, reward, next_state, done):
        """Stores experiences in the replay buffer."""
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        """Returns action based on a given state, following an epsilon-greedy policy."""
        print("epsilon value is ", self.epsilon)
        state_tensor = torch.FloatTensor(state)
        q_values = self.model(state_tensor)
        print("the q values are", q_values.detach().numpy())    
        target_q_values = self.target_model(state_tensor)
        print("the target network values are", target_q_values.detach().numpy())
        if (np.random.rand() <= self.epsilon and self.train_flag):
            print("i selected randomly")
            a = random.randrange(self.action_size)
            # if a == 11 or a == 10:
            #     return 0
            return a
            # return random.randrange(self.action_size)
        # if torch.argmax(q_values).item() == 2:
        #     return 0
        # if torch.argmax(q_values).item() == 10 or torch.argmax(q_values).item() == 11:
        #     return 0
        return torch.argmax(q_values).item()
    
    def test_act(self, states):
        print("I am testing the given states")
        for state in states:
            state_tensor = torch.FloatTensor(state)
            print(state_tensor)
            q_values = self.model(state_tensor)
            print(q_values.detach().numpy())

    def replay(self, batch_size, print_flag):
        """Trains the model using randomly sampled experiences from the replay buffer."""
        self.timesteps_since_last_update += 1
        self.timesteps_since_last_target_update += 1
        if self.timesteps_since_last_update >= self.update_frequency:
            if len(self.memory) >= batch_size:
                minibatch = random.sample(self.memory, batch_size)
            else: 
                return
            for state, action, reward, next_state, done in minibatch:
                target = reward
                if not done:
                    next_state_tensor = torch.FloatTensor(next_state)
                    target_q_values = self.target_model(next_state_tensor).detach()
                    target = reward + self.gamma * torch.max(target_q_values).item()
                state_tensor = torch.FloatTensor(state)
                predicted_q_values = self.model(state_tensor)
                # Compute the loss only for the selected action
                if (print_flag):
                    print(predicted_q_values)
                    print(f"the action selected is {action} with before value {predicted_q_values[0][action]}"\
                    f"and new value {target}")
                    print("the q network values before training are", self.model(state_tensor).detach().numpy())
                predicted_q_values[0][action] = target
                loss = self.criterion(self.model(state_tensor), predicted_q_values)
                if (print_flag):
                    print("loss:", loss.item())
                self.optimizer.zero_grad()
                loss.backward()
                # for i, q_value in enumerate(predicted_q_values[0]):
                #     if i != action:
                #         q_value.grad = None
                # Clip gradients to prevent explosion
                nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                self.optimizer.step()
                if (print_flag):
                    print("the q network values after training are", self.model(state_tensor).detach().numpy())
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay
            self.timesteps_since_last_update = 0

        if self.timesteps_since_last_target_update >= self.target_update_frequency:
            self.target_model.load_state_dict(self.model.state_dict())
            self.timesteps_since_last_target_update = 0
    
    def save_episode(self):
        # Create directory for episodes if it doesn't exist
        episodes_dir = 'DAG/algorithm/DeepJS/episodes/%s' % (self.name)
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

    def save_model(self, store_episode_flag):
        model_dir = 'DAG/algorithm/DeepJS/agents/%s/%s/%s/%s_%s/%s_%s_%s' % (self.name, self.layers, self.learning_rate,
        self.loss, self.activation, self.jobs_num, self.state_size, self.action_size)
        # print(model_dir)
        if store_episode_flag:
            self.save_episode()
        if self.train_flag:
            if not os.path.isdir(model_dir):
                os.makedirs(model_dir)
            model_path = os.path.join(model_dir, 'model.pth')
            torch.save(self.model.state_dict(), model_path)
            # print("i saved the model")

    def load_model(self, model_path):
        checkpoint = torch.load(model_path)
        self.model.load_state_dict(checkpoint)
        # self.model.eval()  # Set the model to evaluation mode
        self.target_model.load_state_dict(self.model.state_dict())

