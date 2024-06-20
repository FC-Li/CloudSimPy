#!/usr/bin/env python3

import os
import sys
import pickle
import argparse

sys.path.append('..')

from playground.DAG.algorithm.DeepJS.DQLAgent import DQLAgent
from playground.DAG.algorithm.DeepJS.DQLScheduler import DQLScheduler
from playground.DAG.algorithm.DeepJS.reward_giver2 import RewardGiver

def main(name, learning_rate, layers, loss, activation, lower_bound, train_flag):
    jobs_num = 92
    exploration = 0.5
    loss_func = loss
    activ_func = activation
    state_features_num = 10
    actions_features_num = 13
    model_dir = f'DAG/algorithm/DeepJS/agents/{name}/{layers}/{learning_rate}/{loss_func}_{activ_func}/{jobs_num}_{state_features_num}_{actions_features_num}'
    model_path = os.path.join(model_dir, 'model.pth')
    print(model_dir, model_path)
    if os.path.exists(model_path):
        agent = DQLAgent(state_features_num, actions_features_num, 0.2, name, jobs_num, layers, learning_rate, loss_func, activ_func, exploration, train_flag)
        agent.load_model(model_path)
        print("Loaded a pre-existing model")
    else:
        agent = DQLAgent(state_features_num, actions_features_num, 0.2, name, jobs_num, layers, learning_rate, loss_func, activ_func, exploration, train_flag)

    episodes_dir = f'DAG/algorithm/DeepJS/episodes/{name}'
    if not os.path.exists(episodes_dir):
        print("no existing directory")
    
    print("the train flag is", train_flag)

    files = os.listdir(episodes_dir)
    num_files = len(files)
    upper_bound = lower_bound + 50
    # for i in range(70, num_files):
    for i in range(lower_bound, upper_bound):
        all_tuples = []
        episode_filename = f'episode_{i}.pkl'
        episode_path = os.path.join(episodes_dir, episode_filename)
        if os.path.exists(episode_path):
            with open(episode_path, 'rb') as f:
                episode_data = pickle.load(f)
                all_tuples.extend(episode_data)
        else:
            print(f"File '{episode_filename}' not found.")
        for state, action, reward, next_state, done in all_tuples:
            agent.remember(state, action, reward, next_state, done)
            agent.replay(16, False)
        # if (i % 3 == 0):
        agent.memory.clear()
    agent.save_model(train_flag)

    agent.test_act([[0.5, 0.5, 0.5, 1, 0, 0, 0, 0, 0, 0],
    [0.5, 0.5, 0, 1, 0, 0, 0, 0, 0, 0],
    [0.5, 0, 0.5, 1, 0, 0, 0, 0, 0, 0],
    [0.5, 1, 0.5, 1, 0, 0.1, 0, 0, 0, 0],
    [0.5, 1, 0.5, 1, 0, 0, 0.1, 0, 0, 1],
    [0.5, 0, 0.5, 1, 0, 0, 0.1, 0, 0, 1],
    [0.8, 0.8, 1, 1, 0, 0.1, 0.1, 0, 1, 0],
    [0.8, 0.8, 1, 1, 0.1, 0.1, 0.1, 1, 0, 0],
    [0.5, 0.5, 0.5, 1, 0.1, 0.1, 0, 1, 1, 0],
    [0.5, 1, 0.5, 1, 0.1, 0.1, 0, 1, 1, 0],
    [1, 1, 0.5, 1, 0.1, 0.1, 0, 1, 1, 0],
    [0.5, 0.5, 0.5, 1, 0, 0.1, 0, 0, 1, 0],
    [0.5, 0.5, 0, 1, 0, 0.1, 0, 0, 1, 0],
    [0.5, 0.5, 0.5, 1, 0, 0, 0.02, 0, 0, 0],
    [0.5, 0.5, 0, 1, 0, 0, 0.02, 0, 0, 1],
    [1, 0.3, 0.1, 1, 0.1, 0, 0, 1, 0, 0],
    [1, 0.5, 0.5, 1, 0.1, 0, 0, 1, 0, 0],
    [0.5, 0, 1, 0, 0.1, 0.01, 0.1, 1, 1, 1],
    [0, 0.5, 1, 0, 0.01, 0.1, 0.1, 1, 1, 1],
    [0, 0, 0.5, 0, 0.01, 0.01, 0.1, 1, 1, 1],
    [0, 0.5, 0.5, 0, 0.001, 0.1, 0.1, 1, 1, 1],
    [0.5, 0.5, 0.5, 0, 0.1, 0.1, 0.1, 1, 1, 1],
    [0.5, 0.3, 0.5, 1, 0.1, 0.1, 0.1, 1, 1, 1],
    [0.5, 1, 0.5, 1, 0.1, 0.1, 0.1, 1, 1, 1],
    [0.8, 0.3, 0.5, 1, 0.1, 0.1, 0.1, 1, 1, 1],
    [1, 1, 0.5, 1, 0.1, 0.1, 0.1, 1, 1, 1],
    [1, 0.5, 0.5, 1, 0.1, 0.1, 0.1, 1, 1, 1],
    [0.5, 0.5, 0.5, 1, 0.1, 0.1, 0.1, 1, 1, 1]]) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run DeepJS with specified learning rate and number of layers.')
    parser.add_argument('name', type=str, help='Name for the reward func components used.')
    parser.add_argument('learning_rate', type=float, help='Learning rate for the neural network.')
    parser.add_argument('layers', type=int, help='Number of layers for the neural network.')
    parser.add_argument('loss', type=str, help='Loss function for the neural network.')
    parser.add_argument('activation', type=str, help='Activation function for the neural network.')
    parser.add_argument('lower_bound', type=int, help='Episodes for usage for the training of the DRL model')
    parser.add_argument('train_flag', type=str, help='Flag for decision for training or testing of the DRL model')
    args = parser.parse_args()

    main(args.name, args.learning_rate, args.layers, args.loss, args.activation, args.lower_bound,  args.train_flag)

