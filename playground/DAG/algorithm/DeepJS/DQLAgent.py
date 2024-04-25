import os
import pickle
import random
from collections import deque

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class QNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, 24)
        self.fc2 = nn.Linear(24, 96)
        self.fc3 = nn.Linear(96, 192)
        self.fc4 = nn.Linear(192, 96)
        self.fc5 = nn.Linear(96, 24)
        self.fc6 = nn.Linear(24, action_size)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = torch.relu(self.fc4(x))
        x = torch.relu(self.fc5(x))
        x = self.fc6(x)
        return x

class DQLAgent:
    def __init__(self, state_size, action_size, gamma, name, layers):
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
        self.update_frequency = 4  # Train the model every 4 timesteps
        self.target_update_frequency = 20
        self.timesteps_since_last_target_update = 0  # Counter for timesteps since last training
        self.timesteps_since_last_update = 0
        self.model = QNetwork(state_size, action_size)
        self.target_model = QNetwork(state_size, action_size)
        self.target_model.load_state_dict(self.model.state_dict())

        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()

    def remember(self, state, action, reward, next_state, done):
        """Stores experiences in the replay buffer."""
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        """Returns action based on a given state, following an epsilon-greedy policy."""
        print("epsilon value is ", self.epsilon)
        state_tensor = torch.FloatTensor(state)
        q_values = self.model(state_tensor)
        print("the q values are", q_values)    
        target_q_values = self.target_model(state_tensor)
        print("the target network values are", target_q_values)
        if np.random.rand() <= self.epsilon:
            print("i selected randomly")
            return random.randrange(self.action_size)
        
        return torch.argmax(q_values).item()
    
    def test_act(self, states):
        print("I am testing the given states")
        for state in states:
            state_tensor = torch.FloatTensor(state)
            q_values = self.model(state_tensor)
            print(q_values)

    def replay(self, batch_size):
        """Trains the model using randomly sampled experiences from the replay buffer."""
        self.timesteps_since_last_update += 1
        self.timesteps_since_last_target_update += 1
        if self.timesteps_since_last_update >= self.update_frequency:
            minibatch = random.sample(self.memory, batch_size)
            for state, action, reward, next_state, done in minibatch:
                target = reward
                if not done:
                    next_state_tensor = torch.FloatTensor(next_state)
                    target_q_values = self.target_model(next_state_tensor).detach()
                    target = reward + self.gamma * torch.max(target_q_values).item()
                state_tensor = torch.FloatTensor(state)
                predicted_q_values = self.model(state_tensor)
                predicted_q_values[0][action] = target
                self.optimizer.zero_grad()
                loss = self.criterion(self.model(state_tensor), predicted_q_values)
                print("loss:", loss.item())
                loss.backward()
                self.optimizer.step()
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay
            self.timesteps_since_last_update = 0

        if self.timesteps_since_last_target_update >= self.target_update_frequency:
            self.target_model.load_state_dict(self.model.state_dict())
            self.timesteps_since_last_target_update = 0
    
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
        model_path = os.path.join(model_dir, 'model.pth')
        torch.save(self.model.state_dict(), model_path)

    def load_model(self, model_path):
        checkpoint = torch.load(model_path)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.eval()  # Set the model to evaluation mode

