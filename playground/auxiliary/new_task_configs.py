import random

def generate_task_instance_configs(task_instances, time, alteration_range=(0.8, 1.2)):
    task_instance_configs = []
    for task_instance in task_instances:
        if time % 100 == 0:
            multiplier = 0.9
        elif time % 50 == 0:
            multiplier = 1.1
        else:
            print("no good time given")
        if task_instance.task_instance_index % 2 == 0:
            mutiplier = 1 / multiplier
        a = task_instance.cpu * multiplier
        b = task_instance.memory * multiplier
        c = task_instance.disk * multiplier
        # a = task_instance.cpu * random.uniform(*alteration_range)
        # b = task_instance.memory * random.uniform(*alteration_range)
        # c = task_instance.disk * random.uniform(*alteration_range)
        
        # Create a new TaskInstanceConfig based on the original, with altered metrics
        altered_metrics = [
            0.0001 if a < 0.0001 else (2 if a > 2 else a),
            0.0001 if b < 0.0001 else (1 if b > 1 else b),
            0.0001 if c < 0.0001 else (1 if c > 1 else c)
        ]
        task_instance.recalc_metrics(altered_metrics)
