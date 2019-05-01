from core.alogrithm import Algorithm


class DRF(Algorithm):
    def __call__(self, cluster, clock):
        machines = cluster.machines
        unfinished_tasks = cluster.unfinished_tasks
        candidate_task = None
        candidate_machine = None

        for machine in machines:
            for task in unfinished_tasks:
                if machine.accommodate(task):
                    candidate_machine = machine
                    candidate_task = task
                    break
        return candidate_machine, candidate_task
