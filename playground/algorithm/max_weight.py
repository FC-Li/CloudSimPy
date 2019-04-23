from playground.utils.feature_synthesize import weights_calculate
from core.alogrithm import Algorithm

class MaxWeightAlgorithm(Algorithm):
    def __call__(self, cluster, clock):
        machines = cluster.machines
        tasks = weights_calculate(cluster.ready_tasks_which_has_waiting_instance)
        candidate_task = None
        candidate_machine = None

        for machine in machines:
            for task in tasks:
                if machine.accommodate(task):
                    candidate_machine = machine
                    candidate_task = task
                    break
        return candidate_machine, candidate_task
