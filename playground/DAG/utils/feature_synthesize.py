import re

def extract_numbers(input_string):
    # Define the regular expression patterns
    first_number_pattern = r'^(\d+)_'
    subsequent_numbers_pattern = r'_(\d+)'

    # Use re.search to find the first number before the first underscore
    first_number_match = re.search(first_number_pattern, input_string)

    # Use re.findall to find all matches of numbers following underscores
    subsequent_numbers_matches = re.findall(subsequent_numbers_pattern, input_string)

    # Convert the matched strings to integers
    first_number = int(first_number_match.group(1)) if first_number_match else None
    subsequent_numbers = [int(match) for match in subsequent_numbers_matches]

    # If there's no underscore, assume the input_string contains only one number
    if '_' not in input_string:
        first_number = float(input_string)

    return first_number, subsequent_numbers

# def father_task_indices(task_id, task_type):
def father_task_indices(task_id):
    father_indices = []
    # print(task_id)
    task_id = str(task_id)
    # print(extract_numbers(task_id))
    task_index, father_indices = extract_numbers(task_id)

    return task_index, father_indices

def task_features(job):
    child_indices = {}
    father_indices = {}
    tasks = job.tasks_map.values()
    
    # Initialize father_indices with all task indices to ensure they exist
    for task in tasks:
        father_indices[task.task_config.task_index] = []

    for task in tasks:
        # print(f"Task {task.task_config.task_index} has parent indices: {task.task_config.parent_indices}")  # For clarity
        task_index = task.task_config.task_index
        task_parent_indices = task.task_config.parent_indices
        child_indices[task_index] = []
        
        for parent_indice in task_parent_indices:
            child_indice = child_indices.setdefault(parent_indice, [])
            child_indice.append(task_index)

    descendant_indices = {}
    for task_index, child_index in child_indices.items():
        descendant_indice = child_index[:]
        for i in child_index:
            descendant_indice += child_indices.get(i, [])  # Use .get() for safer access
        descendant_indice = list(set(descendant_indice))
        descendant_indices[task_index] = descendant_indice

    task_features = {}
    for task_index in child_indices.keys():
        child_index = child_indices[task_index]
        task_feature = task_features.setdefault(task_index, {})
        task_feature['first_layer_task'] = len(child_index)
        task_feature['first_layer_instance'] = 0
        for child in child_index:
            task_feature['first_layer_instance'] += job.tasks_map[child].task_config.instances_number
        task_feature['layers_task'] = 0
        task_feature['child_task_numbers'] = len(descendant_indices[task_index])
        task_feature['child_instance_numbers'] = 0
        for descendant_indice in descendant_indices[task_index]:
            task_feature['child_instance_numbers'] += job.tasks_map[descendant_indice].task_config.instances_number

    queue = []
    for task_index, child_index in child_indices.items():
        if not child_index:
            queue.append(task_index)
            while queue:
                child_node = queue.pop()
                # Debugging: Print the current child_node being processed
                # print(f"Processing child_node: {child_node}")
                father_nodes = father_indices.get(child_node, [])  # Use .get() for safer access
                queue += father_nodes
                for father_node in father_nodes:
                    father_feature = task_features[father_node]
                    child_feature = task_features[child_node]
                    father_feature['layers_task'] = max(father_feature['layers_task'], child_feature['layers_task'] + 1)

    return task_features


def weights_calculate(tasks):
    weight_tasks = {}
    for task in tasks:
        feature = task.feature
        weight = feature['first_layer_task'] + feature['first_layer_instance'] + feature['layers_task'] + feature[
            'child_task_numbers'] + feature['child_instance_numbers']
        task_list = weight_tasks.setdefault(weight, [])
        task_list.append(task)

    sorted_weights = sorted(weight_tasks.keys(), reverse=True)
    sorted_tasks = []
    for weight in sorted_weights:
        sorted_tasks.extend(weight_tasks[weight])

    return sorted_tasks
