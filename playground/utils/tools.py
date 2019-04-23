import time
import numpy as np
import tensorflow as tf

def total_completion(exp):
    min_start_time = 1000000000000
    max_finish_time = -1
    for job in exp.simulation.cluster.jobs:
        for task in job.tasks:
            if task.started_timestamp < min_start_time:
                min_start_time = task.started_timestamp
            if task.finished_timestamp > max_finish_time:
                max_finish_time = task.finished_timestamp
    return (max_finish_time - min_start_time)

def average_completion(exp):
    completion_time = 0
    number_task = 0
    for job in exp.simulation.cluster.jobs:
        for task in job.tasks:
            number_task += 1
            completion_time += (task.finished_timestamp - task.started_timestamp)
    return completion_time / number_task


def average_slowdown(exp):
    slowdown = 0
    number_task = 0
    for job in exp.simulation.cluster.jobs:
        for task in job.tasks:
            number_task += 1
            slowdown += (task.finished_timestamp - task.started_timestamp) / task.task_config.duration
    return slowdown / number_task


def multiprocessing_run(episode, trajectories, makespans, average_completions, average_slowdowns):
    np.random.seed(int(time.time()))
    tf.random.set_random_seed(time.time())
    episode.run()
    trajectories.append(episode.simulation.scheduler.algorithm.current_trajectory)
    makespans.append(episode.simulation.env.now)
    # print(episode.simulation.env.now)
    average_completions.append(average_completion(episode))
    average_slowdowns.append(average_slowdown(episode))
