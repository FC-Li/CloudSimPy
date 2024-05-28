#!/usr/bin/env python3

import os
import time
import numpy as np
import tensorflow as tf
import sys
import argparse

os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'
sys.path.append('..')

from core.machine import MachineConfig
from core.node import Node
from playground.DAG.algorithm.heuristics.random_algorithm import RandomAlgorithm
from playground.DAG.algorithm.heuristics.tetris import Tetris
from playground.DAG.algorithm.heuristics.first_fit import FirstFitAlgorithm
from playground.DAG.algorithm.heuristics.best_fit import BestFitAlgorithm
from playground.DAG.algorithm.heuristics.max_weight import MaxWeightAlgorithm

from playground.DAG.algorithm.DeepJS.DRL import RLAlgorithm
from playground.DAG.algorithm.DeepJS.agent import Agent
from playground.DAG.algorithm.DeepJS.brain import BrainSmall
from playground.DAG.algorithm.DeepJS.reward_giver import MakespanRewardGiver

from playground.DAG.utils.csv_reader import CSVReader
from playground.DAG.utils.feature_functions import features_extract_func_ac, features_normalize_func_ac
from playground.auxiliary.tools import average_completion, average_slowdown
from playground.DAG.adapter.episode import Episode

def main(method, algorithm, name, learning_rate, layers, loss, activation):

    os.environ['CUDA_VISIBLE_DEVICES'] = ''

    np.random.seed(41)
    tf.random.set_seed(41)
    # ************************ Parameters Setting Start ************************
    machines_number = [70, 95 , 140] 
    '''
    near_edge_machines_number = 30
    far_edge_machines_number = 40
    cloud_machines_number = 100
    '''

    n_iter = 30
    jobs_csv = os.path.join("DAG", "jobs_files", "small_modified_jobs.csv")
    # jobs_csv = os.path.join("DAG", "jobs_files", "3_jobs.csv")

    machine_groups = {}  # Dictionary to hold lists of machines grouped by node_id
    for cluster_index, top_machines_number in enumerate(machines_number):
        for node_id in range(top_machines_number // 3):
            # Use a tuple of (cluster_index, node_id) as the key to ensure uniqueness
            key = (cluster_index, node_id)

            # Initialize the list for each unique (cluster_index, node_id) if not already done
            if key not in machine_groups:
                machine_groups[key] = []
            # Add machines to the appropriate group identified by the unique key
            machine_groups[key].extend(
                [MachineConfig(3, 3, 1, cluster_index, node_id) for _ in range(3)]
            )

    node_configs = [Node(node_id, cluster_index) 
                    for cluster_index, top_machines_number in enumerate(machines_number) 
                    for node_id in range(top_machines_number // 3)]
                    
    # csv_reader = CSVReader(jobs_csv)
    # jobs_configs = csv_reader.generate(0, 9)

    tic = time.time()
    if algorithm == 'FirstFit':
        algorithm = FirstFitAlgorithm()
    elif algorithm == 'BestFit':
        algorithm = BestFitAlgorithm()
    
    episode = Episode(machine_groups, machines_number, node_configs, jobs_csv, method, algorithm, name, learning_rate, layers, \
    loss, activation, None)
    episode.run()
    if algorithm == 'FirstFit':
        print('FirstFitAlgorithm')
    elif algorithm == 'BestFit':
        print('BestFitAlgorithm')

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run DeepJS with specified learning rate and number of layers.')
    parser.add_argument('method', type=int, help='Select the method of your testing env')
    parser.add_argument('algorithm', type=str, help='Select the Algorithm for the job allocation.')
    parser.add_argument('name', type=str, help='Name for the reward func components used.')
    parser.add_argument('learning_rate', type=float, help='Learning rate for the neural network.')
    parser.add_argument('layers', type=int, help='Number of layers for the neural network.')
    parser.add_argument('loss', type=str, help='Loss function for the neural network.')
    parser.add_argument('activation', type=str, help='Activation function for the neural network.')
    args = parser.parse_args()

    main(args.method, args.algorithm, args.name, args.learning_rate, args.layers, args.loss, args.activation)
