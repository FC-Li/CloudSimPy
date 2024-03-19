def print_selected_task_instances(task_instances, str):
    tasks_list = []
    for task_instance in task_instances:
        if task_instance.machine != None:
            tasks_list.append((task_instance.task.job.id, \
            task_instance.task.task_index, task_instance.task_instance_index, task_instance.machine.id))
        else:
            tasks_list.append((task_instance.task.job.id, \
            task_instance.task.task_index, task_instance.task_instance_index, None))
    print(f"{str} task_instances: {tasks_list}")