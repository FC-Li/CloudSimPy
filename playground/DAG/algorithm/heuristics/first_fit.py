from core.alogrithm import Algorithm


class FirstFitAlgorithm(Algorithm):
    def __call__(self, cluster, clock):
        machines = cluster.machines
        tasks = cluster.ready_tasks_which_has_waiting_instance
        matched_items = []
        unmatched_tasks = []

        for task in tasks:
            for task_instance in task.task_instances:
                matched = False  # Flag to indicate if the task has been matched
                for machine in machines:
                    if machine.accommodate(task_instance):
                        print('task instance %s of task %s of job %s was allocated to machine %f' % (task_instance.task_instance_index, task.task_config.task_index, task.job.job_config.id, machine.id))
                        task.start_task_instance(machine)
                        matched_items.append((machine, task_instance))  # Corrected to append a tuple
                        matched = True
                        break  # Exit the inner loop if a match is found
                if not matched:
                    # Only add the task to unmatched_tasks if no match was found after checking all machines
                    unmatched_tasks.append(task)
                    break

                    
        return matched_items, unmatched_tasks
