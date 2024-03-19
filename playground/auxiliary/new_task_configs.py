import random

def generate_task_instance_configs(task_instances, alteration_range=(0.8, 1.2)):
    task_instance_configs = []
    for task_instance in task_instances:
        a = task_instance.cpu * random.uniform(*alteration_range)
        b = task_instance.memory * random.uniform(*alteration_range)
        c = task_instance.disk * random.uniform(*alteration_range)
        
        # Create a new TaskInstanceConfig based on the original, with altered metrics
        altered_metrics = [
            0.0001 if a < 0.0001 else (2 if a > 2 else a),
            0.0001 if b < 0.0001 else (1 if b > 1 else b),
            0.0001 if c < 0.0001 else (1 if c > 1 else c)
        ]
        task_instance.recalc_metrics(altered_metrics)
