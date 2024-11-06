import numpy as np

class TaskInstanceConfig(object):
    def __init__(self, task_config):
        self.cpu = task_config.cpu
        self.memory = task_config.memory
        self.disk = task_config.disk
        self.duration = task_config.duration
        self.response_time = task_config.response_time
        self.before_0_response_time = 1000
        # self.before_0_response_time = np.random.uniform(0, 5000)


class TaskConfig(object):
    def __init__(self, task_index, instances_number, cpu, memory, disk, \
    duration, response_time, submit_time, cnt_all_instances, parent_indices=None):
        self.task_index = task_index
        self.instances_number = instances_number
        self.cpu = cpu
        self.memory = memory
        self.disk = disk
        self.duration = duration
        self.response_time = response_time
        self.submit_time = submit_time
        self.parent_indices = parent_indices
        self.cnt_all_instances = cnt_all_instances
        # self.response_time_threshold = np.random.uniform(5, 1000)


class JobConfig(object):
    def __init__(self, idx, submit_time, response_time, type, response_time_rtt, task_configs):
        self.submit_time = submit_time
        self.response_time = response_time
        self.task_configs = task_configs
        self.id = idx
        self.type = type
        self.response_time_rtt = response_time_rtt
