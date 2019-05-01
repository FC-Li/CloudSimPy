from core.alogrithm import Algorithm


class FirstFitAlgorithm(Algorithm):
    def __call__(self, cluster, clock):
        machines = cluster.machines
        tasks = cluster.ready_tasks_which_has_waiting_instance
        candidate_task = None
        candidate_machine = None

        for machine in machines:
            for task in tasks:
                if machine.accommodate(task):
                    candidate_machine = machine
                    candidate_task = task
                    break
        return candidate_machine, candidate_task
