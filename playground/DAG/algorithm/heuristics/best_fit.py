from core.alogrithm import Algorithm

class BestFitAlgorithm(Algorithm):
    def __call__(self, cluster, env):
        clock = env.now
        self.env = env
        time_threshold = 50
        div = clock // time_threshold
        if clock == 0:
            time_threshold = 50
        else:
            time_threshold = (div+1) * time_threshold

        while ((self.env.now + 0.6) / time_threshold < 1):
            machines = [machine for node in cluster.nodes for machine in node.machines if machine.num_waiting_instances == 0]
            tasks = cluster.ready_tasks_which_has_waiting_instance

            for task in tasks:
                for task_instance in task.unscheduled_task_instances:
                    best_machine = None
                    min_capacity_diff = float('inf')  # Initialize with infinity
                    for machine in machines:
                        if machine.accommodate(task_instance):
                            capacity_diff = machine.capacity_difference(task_instance)
                            if capacity_diff < min_capacity_diff:
                                min_capacity_diff = capacity_diff
                                best_machine = machine
                    if best_machine:
                        task_instance.passive_refresh_response_time(self.env.now - task.job.job_config.submit_time + task_instance.config.response_time)
                        task.start_task_instance(task_instance.task_instance_index, best_machine)
            yield self.env.timeout(0.5)

        return
