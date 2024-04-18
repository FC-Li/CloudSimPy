from core.alogrithm import Algorithm


class FirstFitAlgorithm(Algorithm):
    def __call__(self, cluster, env):

        clock = env.now
        self.env = env
        time_threshold = 50
        div = clock // time_threshold
        if clock == 0:
            time_threshold = 50
        else:
            time_threshold = (div+1) * time_threshold # ama einai estw kai 0.1 over tote pausarei sto epomeno checkpoint

        while ((self.env.now + 0.6) / time_threshold < 1):
            # if (num_running_instances != len(cluster.running_task_instances))

            machines = [machine for node in cluster.nodes for machine in node.machines if machine.num_waiting_instances == 0]
            tasks = cluster.ready_tasks_which_has_waiting_instance

            # print("the time in this allocation attempt is", self.env.now)

            for task in tasks:
                for task_instance in task.unscheduled_task_instances:
                    # if task_instance.has_been_reallocated:
                    #     print("I am a transferred instance that tries to be allocated to a machine")
                    matched = False  # Flag to indicate if the task has been matched
                    for machine in machines:
                        if machine.accommodate(task_instance):
                            # print('task instance %s of task %s of job %s was allocated to machine %f of the cluster %f with submit time %f ' \
                            # 'at time %d' % (task_instance.task_instance_index, task.task_config.task_index, task.job.job_config.id, machine.id, cluster.level, \
                            # task.task_config.submit_time, self.env.now))
                            task_instance.passive_refresh_response_time(self.env.now - task.job.job_config.submit_time + task_instance.config.response_time)
                            task.start_task_instance(task_instance.task_instance_index, machine)
                            matched = True
                            break  # Exit the inner loop if a match is found
                        # else: print(task_instance.cpu, task_instance.memory, task_instance.disk)
                    if not matched:
                            task_instance.passive_refresh_response_time(self.env.now - task.job.job_config.submit_time + task_instance.config.response_time)
                        # break
            # num_running_instances = len(cluster.running_task_instances)
            yield self.env.timeout(0.5) 

        # print('I just executed the first fit... for cluster', cluster.level, 'at time', self.env.now)
        return
