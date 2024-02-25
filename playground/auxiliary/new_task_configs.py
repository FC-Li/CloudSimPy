import random

def generate_task_instance_configs(tasks, alteration_range=(0.8, 1.2)):
    task_instance_configs = []
    for task in tasks:
        for task_instance in task.running_task_instances:
            # Create a new TaskInstanceConfig based on the original, with altered metrics
            altered_metrics = [
                task_instance.cpu * random.uniform(*alteration_range),
                task_instance.memory * random.uniform(*alteration_range),
                task_instance.disk * random.uniform(*alteration_range),
            ]
            task_instance.recalc_metrics(altered_metrics)
