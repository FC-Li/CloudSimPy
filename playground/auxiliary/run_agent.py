import os
import sys
import pickle

sys.path.append('..')

from playground.DAG.algorithm.DeepJS.DQLAgent import DQLAgent
from playground.DAG.algorithm.DeepJS.DQLScheduler import DQLScheduler
from playground.DAG.algorithm.DeepJS.reward_giver2 import RewardGiver

jobs_num = 90
state_features_num = 10
actions_features_num = 13
layers = 6
model_dir = 'DAG/algorithm/DeepJS/agents/%s/all/%s_%s_%s' % (layers, jobs_num, state_features_num, actions_features_num)
model_path = os.path.join(model_dir, 'model.pth')  # Change from 'model.h5' to 'model.pth'
print(model_dir, model_path)
if os.path.exists(model_path):
    agent = DQLAgent(state_features_num, actions_features_num, 0.9, jobs_num, layers)
    agent.load_model(model_path)
    print("Loaded a pre-existing model")
else:
    agent = DQLAgent(state_features_num, actions_features_num, 0.9, jobs_num, layers)

agent.test_act([[0.5, 0.5, 0.5, 1, 0, 0, 0, 0, 0, 0],
[0.5, 1, 0.5, 1, 0, 0.1, 0, 0, 0, 0],
[0.5, 1, 0.5, 1, 0, 0, 0.001, 0, 0, 1],
[0.5, 0.5, 0.5, 1, 0.5, 0.001, 0, 1, 1, 0],
[0.5, 0.5, 0.5, 1, 0, 0.02, 0, 0, 1, 0],
[0.5, 0.5, 0.5, 1, 0, 0, 0.02, 0, 0, 0],
[0.5, 0.5, 0.5, 1, 0.02, 0.1, 0.1, 1, 1, 1],
[0.5, 0.5, 0.5, 0, 0.02, 0.1, 0.1, 1, 1, 1],
[1, 0.5, 0.5, 0, 0.02, 0.1, 0.1, 1, 1, 1],
[0.5, 0.5, 1, 0, 0.02, 0.1, 0.1, 1, 1, 1],
[0.5, 0.5, 1, 1, 0.02, 0.1, 0.1, 1, 1, 1],
[0.5, 1, 1, 1, 0.02, 0.1, 0.1, 1, 1, 1]]) 


episodes_dir = 'DAG/algorithm/DeepJS/episodes'
if not os.path.exists(episodes_dir):
    print("no existing directory")
# Find the first available episode number
files = os.listdir(episodes_dir)
# Count the number of files
num_files = len(files)
# num_files = 20
for i in range(1, num_files):
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
        agent.replay(10, False)
        agent.save_model(False)
