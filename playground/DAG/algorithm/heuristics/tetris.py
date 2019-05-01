import numpy as np
from core.alogrithm import Algorithm


class Tetris(Algorithm):
    @staticmethod
    def calculate_alignment(valid_pairs):
        machine_features = []
        task_features = []
        for index, pair in enumerate(valid_pairs):
            machine = pair[0]
            task = pair[1]
            machine_features.append(machine.feature[:2])
            task_features.append([task.task_config.cpu, task.task_config.memory])
        return np.argmax(np.sum(np.array(machine_features) * np.array(task_features), axis=1), axis=0)

    def __call__(self, cluster, clock):
        machines = cluster.machines
        tasks = cluster.ready_tasks_which_has_waiting_instance
        valid_pairs = []
        for machine in machines:
            for task in tasks:
                if machine.accommodate(task):
                    valid_pairs.append((machine, task))
        if len(valid_pairs) == 0:
            return None, None
        pair_index = Tetris.calculate_alignment(valid_pairs)
        pair = valid_pairs[pair_index]
        return pair[0], pair[1]
