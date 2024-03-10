from core.alogrithm import Algorithm
from playground.auxiliary.remove_delays import remove_delays


class FirstFitAlgorithm(Algorithm):
    def __call__(self, cluster, env):

        clock = env.now
        self.env = env
        time_threshold = 300
        div = clock / time_threshold
        if clock == 0:
            time_threshold = 300
        elif ((clock % time_threshold) == 0):
            time_threshold = (div) * time_threshold # ama einai akrivws 300,600 klp tote paw sto pause
        else:
            time_threshold = (div+1) * time_threshold # ama einai estw kai 0.1 over tote pausarei sto epomeno checkpoint

        while ((self.env.now) / time_threshold < 1 or self.env.now == 0):
            # if (num_running_instances != len(cluster.running_task_instances))

            machines = [machine for node in cluster.nodes for machine in node.machines if machine.num_waiting_instances == 0]
            tasks = cluster.ready_tasks_which_has_waiting_instance

            for task in tasks:
                for task_instance in task.unscheduled_task_instances:
                    matched = False  # Flag to indicate if the task has been matched
                    for machine in machines:
                        if machine.accommodate(task_instance):
                            print('task instance %s of task %s of job %s was allocated to machine %f of the cluster %f with submit time %f' \
                            % (task_instance.task_instance_index, task.task_config.task_index, task.job.job_config.id, machine.id, cluster.level, \
                            task.task_config.submit_time))
                            # task_instance.passive_refresh_response_time(remove_delays(task.job.job_config.submit_time, self.env.now))
                            task_instance.passive_refresh_response_time(self.env.now - task.job.job_config.submit_time)
                            task.start_task_instance(task_instance.task_instance_index, machine)
                            matched = True
                            break  # Exit the inner loop if a match is found
                        # else: print(task_instance.cpu, task_instance.memory, task_instance.disk)
                    if not matched:
                        # Only add the task to unmatched_tasks if no match was found after checking all machines
                            # task_instance.passive_refresh_response_time(remove_delays(task.job.job_config.submit_time, self.env.now))
                            task_instance.passive_refresh_response_time(self.env.now - task.job.job_config.submit_time)
                        # break
            num_running_instances = len(cluster.running_task_instances)
            yield self.env.timeout(1) 



        print('I just executed the first fit... for cluster', cluster.level)
        return
