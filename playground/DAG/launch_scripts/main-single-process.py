import os
import time
import numpy as np
import tensorflow as tf
import sys

os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'
sys.path.append('..')

from core.machine import MachineConfig
from playground.DAG.algorithm.heuristics.random_algorithm import RandomAlgorithm
from playground.DAG.algorithm.heuristics.tetris import Tetris
from playground.DAG.algorithm.heuristics.first_fit import FirstFitAlgorithm
from playground.DAG.algorithm.heuristics.max_weight import MaxWeightAlgorithm

from playground.DAG.algorithm.DeepJS.DRL import RLAlgorithm
from playground.DAG.algorithm.DeepJS.agent import Agent
from playground.DAG.algorithm.DeepJS.brain import BrainSmall
from playground.DAG.algorithm.DeepJS.reward_giver import MakespanRewardGiver

from playground.DAG.utils.csv_reader import CSVReader
from playground.DAG.utils.feature_functions import features_extract_func_ac, features_normalize_func_ac
from playground.auxiliary.tools import average_completion, average_slowdown
from playground.DAG.adapter.episode import Episode

os.environ['CUDA_VISIBLE_DEVICES'] = ''

np.random.seed(41)
tf.random.set_seed(41)
# ************************ Parameters Setting Start ************************
machines_number = 100
jobs_len = 200
n_iter = 30
jobs_csv = os.path.join("DAG", "jobs_files", "job.csv")

machine_configs = [MachineConfig(2, 1, 1) for i in range(machines_number)]
csv_reader = CSVReader(jobs_csv)
jobs_configs = csv_reader.generate(0, 9)


# Start the control process as a background thread
# control_thread = threading.Thread(target=control_process)
# control_thread.start()

tic = time.time()
algorithm = FirstFitAlgorithm()
episode = Episode(machine_configs, jobs_configs, algorithm, None)
episode.run()
print('FirstFitAlgorithm')
print(episode.env.now, time.time() - tic, average_completion(episode), average_slowdown(episode))

# brain = BrainSmall(14)
# reward_giver = MakespanRewardGiver(-1)
# features_extract_func = features_extract_func_ac
# features_normalize_func = features_normalize_func_ac

# name = '%s-%s-m%d' % (reward_giver.name, brain.name, machines_number)
# model_dir = './agents/%s' % name
# ************************ Parameters Setting End ************************

# if not os.path.isdir(model_dir):
#     os.makedirs(model_dir)

# agent = Agent(name, brain, 1, reward_to_go=True, nn_baseline=True, normalize_advantages=True,
#               model_save_path='%s/model.ckpt' % model_dir)

# tic = time.time()
# algorithm = RandomAlgorithm()
# episode = Episode(machine_configs, jobs_configs, algorithm, None)
# episode.run()
# print('RandomAlgorithm')
# print(episode.env.now, time.time() - tic, average_completion(episode), average_slowdown(episode))

# tic = time.time()
# algorithm = Tetris()
# episode = Episode(machine_configs, jobs_configs, algorithm, None)
# episode.run()
# print('Tetris')
# print(episode.env.now, time.time() - tic, average_completion(episode), average_slowdown(episode))
# tic = time.time()
# algorithm = MaxWeightAlgorithm()
# episode = Episode(machine_configs, jobs_configs, algorithm, None)
# episode.run()
# print('MaxWeightAlgorithm')
# print(episode.env.now, time.time() - tic, average_completion(episode), average_slowdown(episode))

# for itr in range(n_iter):
#     print("********** Iteration %i ************" % itr)
#     all_observations = []
#     all_actions = []
#     all_rewards = []

#     makespans = []
#     average_completions = []
#     average_slowdowns = []
#     trajectories = []

#     tic = time.time()
#     for i in range(12):
#         algorithm = RLAlgorithm(agent, reward_giver, features_extract_func=features_extract_func,
#                                 features_normalize_func=features_normalize_func)
#         episode = Episode(machine_configs, jobs_configs, algorithm, None)
#         algorithm.reward_giver.attach(episode.simulation)
#         episode.run()
#         trajectories.append(episode.simulation.scheduler.algorithm.current_trajectory)
#         makespans.append(episode.simulation.env.now)
#         average_completions.append(average_completion(episode))
#         average_slowdowns.append(average_slowdown(episode))

#     agent.log('makespan', np.mean(makespans), agent.global_step)
#     agent.log('average_completions', np.mean(average_completions), agent.global_step)
#     agent.log('average_slowdowns', np.mean(average_slowdowns), agent.global_step)

#     toc = time.time()
#     print(np.mean(makespans), (toc - tic) / 12, np.mean(average_completions), np.mean(average_slowdowns))

#     for trajectory in trajectories:
#         observations = []
#         actions = []
#         rewards = []
#         for node in trajectory:
#             observations.append(node.observation)
#             actions.append(node.action)
#             rewards.append(node.reward)

#         all_observations.append(observations)
#         all_actions.append(actions)
#         all_rewards.append(rewards)

#     all_q_s, all_advantages = agent.estimate_return(all_rewards)
#     agent.update_parameters(all_observations, all_actions, all_advantages)

# agent.save()
