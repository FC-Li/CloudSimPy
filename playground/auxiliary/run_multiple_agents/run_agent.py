import os
import sys
import pickle

sys.path.append('..')

from playground.DAG.algorithm.DeepJS.DQLAgent import DQLAgent
from playground.DAG.algorithm.DeepJS.DQLScheduler import DQLScheduler
from playground.DAG.algorithm.DeepJS.reward_giver2 import RewardGiver

jobs_num = 92
loss_func = "MSE"
activ_func = "ReLU"
state_features_num = 10
actions_features_num = 13
layers = 6
learning_rate = 0.0001
name = "all"
model_dir = 'DAG/algorithm/DeepJS/agents/%s/%s/%s/%s_%s/%s_%s_%s' % (name, layers, learning_rate,
loss_func, activ_func, jobs_num, state_features_num, actions_features_num)
model_path = os.path.join(model_dir, 'model.pth')  # Change from 'model.h5' to 'model.pth'
print(model_dir, model_path)
if os.path.exists(model_path):
    agent = DQLAgent(state_features_num, actions_features_num, 0.9, name, jobs_num, layers, learning_rate, loss_func, activ_func)
    agent.load_model(model_path)
    print("Loaded a pre-existing model")
else:
    agent = DQLAgent(state_features_num, actions_features_num, 0.9, name, jobs_num, layers, learning_rate, loss_func, activ_func)

agent.test_act([[0.5, 0.5, 0.5, 1, 0, 0, 0, 0, 0, 0],
[0.5, 0.5, 0, 1, 0, 0, 0, 0, 0, 0],
[0.5, 0, 0.5, 1, 0, 0, 0, 0, 0, 0],
[0.5, 1, 0.5, 1, 0, 0.1, 0, 0, 0, 0],
[0.5, 1, 0.5, 1, 0, 0, 0.001, 0, 0, 1],
[0.5, 0, 0.5, 1, 0, 0, 0.001, 0, 0, 1],
[0.8, 0.8, 1, 1, 0, 0.1, 0.1, 0, 1, 0],
[0.8, 0.8, 1, 1, 0.02, 0.1, 0.1, 1, 0, 0],
[0.5, 0.5, 0.5, 1, 0.5, 0.001, 0, 1, 1, 0],
[0.5, 1, 0.5, 1, 0.5, 0.001, 0, 1, 1, 0],
[1, 1, 0.5, 1, 0.5, 0.001, 0, 1, 1, 0],
[0.5, 0.5, 0.5, 1, 0, 0.02, 0, 0, 1, 0],
[0.5, 0.5, 0, 1, 0, 0.02, 0, 0, 1, 0],
[0.5, 0.5, 0.5, 1, 0, 0, 0.02, 0, 0, 0],
[0.5, 0.5, 0, 1, 0, 0, 0.02, 0, 0, 1],
[0.5, 0.5, 0.5, 1, 0.02, 0.1, 0.1, 1, 1, 1],
[0.5, 0.5, 0.5, 0, 0.02, 0.1, 0.1, 1, 1, 1],
[0.5, 0.5, 1, 0, 0.02, 0.1, 0.5, 1, 1, 1],
[0.5, 0.3, 0.5, 1, 0.02, 0.1, 0.1, 1, 1, 1],
[0.5, 1, 0.5, 1, 0.02, 0.1, 0.1, 1, 1, 1],
[1, 0.5, 0.5, 1, 0.02, 0.1, 0.1, 1, 1, 1],
[1, 0.3, 0.1, 1, 0.02, 0, 0, 1, 0, 0],
[1, 0.5, 0.5, 1, 0.02, 0, 0, 1, 0, 0],
[0.5, 0.5, 1, 1, 0.02, 0.1, 0.5, 1, 1, 1],
[0.5, 1, 1, 1, 0.02, 0.1, 0.5, 1, 1, 1]]) 


episodes_dir = 'DAG/algorithm/DeepJS/episodes/%s' % (name)
if not os.path.exists(episodes_dir):
    print("no existing directory")
# Find the first available episode number
files = os.listdir(episodes_dir)
# Count the number of files
num_files = len(files) + 100
# num_files = 20
for i in range(1, num_files):
    # if i > 1:
    #     agent = DQLAgent(state_features_num, actions_features_num, 0.9, jobs_num, layers)
    #     agent.load_model(model_path)
    # i += 68
    all_tuples = []
    episode_filename = f'episode_{i}.pkl'
    episode_path = os.path.join(episodes_dir, episode_filename)
    if os.path.exists(episode_path):
        with open(episode_path, 'rb') as f:
            # Load the contents of the pickle file
            episode_data = pickle.load(f)
            all_tuples.extend(episode_data)
    else:
        print(f"File '{episode_filename}' not found.")
    for state, action, reward, next_state, done in all_tuples:
        agent.remember(state, action, reward, next_state, done)
        agent.replay(20, False)
    if (i % 10 == 0):
        agent.memory.clear() # Replay buffer
    agent.save_model(False)
