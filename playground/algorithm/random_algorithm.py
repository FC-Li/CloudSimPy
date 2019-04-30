import numpy as np
from core.alogrithm import Algorithm


class RandomAlgorithm(Algorithm):
    def __init__(self, threshold=0.8):
        self.threshold = threshold

    def __call__(self, cluster, clock):
        machines = cluster.machines
        tasks = cluster.ready_tasks_which_has_waiting_instance
        candidate_task = None
        candidate_machine = None
        all_candidates = []

        for machine in machines:
            for task in tasks:
                if machine.accommodate(task):
                    all_candidates.append((machine, task))
                    if np.random.rand() > self.threshold:
                        candidate_machine = machine
                        candidate_task = task
                        break
        if len(all_candidates) == 0:
            return None, None
        if candidate_task is None:
            pair_index = np.random.randint(0, len(all_candidates))
            return all_candidates[pair_index]
        else:
            return candidate_machine, candidate_task
