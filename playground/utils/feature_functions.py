import numpy as np


def features_extract_func(task):
    return [task.task_config.cpu, task.task_config.memory,
            task.task_config.duration, task.waiting_task_instances_number,
            task.feature['first_layer_task'], task.feature['first_layer_instance'],
            task.feature['layers_task'], task.feature['child_task_numbers'],
            task.feature['child_instance_numbers']]

def features_extract_func_ac(task):
    return features_extract_func(task) + [task.task_config.instances_number, len(task.running_task_instances),
                                          len(task.finished_task_instances)]


def features_normalize_func(x):
    y = (np.array(x) - np.array([0, 0, 0.65, 0.009, 74.0, 80.3])) / np.array([64, 1, 0.23, 0.005, 108.0, 643.5])
    return y


def features_normalize_func_ac(x):
    y = (np.array(x) - np.array([0, 0, 0.65, 0.009, 74.0, 80.3, 80.3, 80.3, 80.3])) / np.array(
        [64, 1, 0.23, 0.005, 108.0, 643.5, 643.5, 643.5, 643.5])
    return y
