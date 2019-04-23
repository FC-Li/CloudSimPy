#父节点信息提取
def father_task_indexs(task_id, task_type):
	father_indices = []

	if (task_id.find('task_') != -1) :
		task_index = task_type+'_'+'task_id'
		return (task_index, father_indices)

	numList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	start_index = -1

	for i, char_s in enumerate(task_id):
		if (char_s in numList) and (start_index == -1):
			start_index = i
		if (char_s not in numList) and (start_index != -1):
			father_indice = task_type + '_' + task_id[start_index: i]
			father_indices.append(father_indice)
			start_index = -1

	if (start_index != -1):
		father_indice = task_type + '_' + task_id[start_index:]
		father_indices.append(father_indice)


	task_index = father_indices[0]
	father_indices = father_indices[1:]

	return (task_index, father_indices)

#子节点特征提取
def task_features(job):
	child_indices = {}
	father_indices = {}
	tasks = job.tasks_map.values()
	for task in tasks:
		task_index = task.task_config.task_index
		task_parent_indices = task.task_config.parent_indices
		father_indices[task_index] = task_parent_indices
		child_indices[task_index] = []
		for parent_indice in task_parent_indices:
			child_indice = child_indices.setdefault(parent_indice, [])
			child_indice.append(task_index)

	descendant_indices = {}
	descendant_indice = []
	for task_index, child_index in child_indices.items():
		descendant_indice = child_index[:]
		for i in child_index:
			descendant_indice += child_indices[i]
		descendant_indice = list(set(descendant_indice))
		descendant_indices.update({task_index: descendant_indice})

	task_features = {}
	queue = []
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

	# print(father_indices)
	# print(child_indices)
	# print(descendant_indices)
	for task_index, child_index in child_indices.items():

		if not child_index:
			queue.append(task_index)

			while queue:
				child_node = queue.pop()
				# print('************')
				# print(child_node)
				father_nodes = father_indices[child_node]
				queue += father_nodes
				for father_node in father_nodes:
					father_feature = task_features[father_node]
					child_feature = task_features[child_node]
					father_feature['layers_task'] = child_feature['layers_task']+1 if father_feature['layers_task']==0 else max(father_feature['layers_task'], child_feature['layers_task']+1)


	return task_features

#权值计算
def weights_calculate(tasks):
	weight_tasks = {}
	for task in tasks:
		feature = task.feature
		weight = feature['first_layer_task'] + feature['first_layer_instance'] + feature['layers_task'] + feature['child_task_numbers'] + feature['child_instance_numbers'] 
		task_list = weight_tasks.setdefault(weight, [])
		task_list.append(task)

	sorted_weights = sorted(weight_tasks.keys(), reverse=True)
	sorted_tasks = []
	for weight in sorted_weights:
		sorted_tasks.extend(weight_tasks[weight])

	return sorted_tasks