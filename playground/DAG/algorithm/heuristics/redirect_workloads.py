from playground.auxiliary import remove_delays


def extract_workloads(self, cluster, clock, algorithm, machine_sort_key):
    machines = cluster.machines
    tasks = # i will tell you who the tasks are in a list and also say how many instances are in them
    matched_items = []
    unmatched_tasks = []

    for task in sorted_tasks:
        for task_instance in task.task_instances:
            matched = False  # Flag to indicate if the task has been matched
            sorted_machines = sorted_machines(machines, algorithm)
        
            for machine in sorted_machines:
                if machine.accommodate(task_instance):
                    print('task instance %s of task %s of job %s was allocated to machine %f of the cluster %f' \
                    % (task_instance.task_instance_index, task.task_config.task_index, task.job.job_config.id, machine.id, cluster.level))
                    if (task_instance.response_time != 0):
                        print("I have response time greater than 0")
                        task_instance.refresh_response_time(remove_delays(task.job.job_config.submit_time, clock))
                    task.start_task_instance(machine)
                    matched_items.append((machine, task_instance))  # Corrected to append a tuple
                    matched = True
                    break  # Exit the inner loop if a match is found
            if not matched:
                # Only add the task to unmatched_tasks if no match was found after checking all machines
                for i in range((int(task.next_instance_pointer)), int(task.task_config.instances_number)):
                    task_instance.refresh_response_time(remove_delays(task.job.job_config.submit_time, clock))
                    task.task_instances[i].passive_refresh_response_time(response_time)
                unmatched_tasks.append(task)
                break

    print('I just executed the first fit... for cluster', cluster.level)
    return matched_items, unmatched_tasks
