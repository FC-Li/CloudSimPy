def sorted_machines(machines, algorithm):
    sorted_node_id = sorted(machines, key=lambda machine: machine.node_id)
    if algorithm == util:
        max_tuple = (0.0,0)
        for i in range(0, len(sorted_node_id), 3):
            avg_usage = 0.0
            node_id = sorted_node_id[0].node_id
            node_machines = sorted_node_id[i:i+3]
            for machine in node_machines:
                avg_usage += machine.avg_usage()
            avg_usage = avg_usage / 3
            if avg_usage > max_tuple[0]:
                max_tuple = (avg_usage, node_id)
        return max_tuple[1]
    if algorithm == scheduled_time:
        min_tuple = (1000000.0,0)
        for i in range(0, len(sorted_node_id), 3):
            avg_time = 0.0
            node_id = sorted_node_id[0].node_id
            node_machines = sorted_node_id[i:i+3]
            for machine in node_machines:
                avg_time += machine.scheduled_time()
            avg_time = avg_time / 3
            if avg_time < min_tuple[0]:
                min_tuple = (avg_time, node_id)
        return min_tuple[1]
    if algorithm == remaining_time:
        min_tuple = (1000000.0,0)
        for i in range(0, len(sorted_node_id), 3):
            avg_time = 0.0
            node_id = sorted_node_id[0].node_id
            node_machines = sorted_node_id[i:i+3]
            for machine in node_machines:
                avg_time += machine.remaining_time()
            avg_time = avg_time / 3
            if avg_time < min_tuple[0]:
                min_tuple = (avg_time, node_id)
        return min_tuple[1]
    if algorithm == active_workloads:
        max_tuple = (0.0,0)
        for i in range(0, len(sorted_node_id), 3):
            avg_num = 0.0
            node_id = sorted_node_id[0].node_id
            node_machines = sorted_node_id[i:i+3]
            for machine in node_machines:
                avg_num += len(machine.running_task_instances())
            avg_num = avg_num / 3
            if avg_num > max_tuple[0]:
                max_tuple = (avg_num, node_id)
        return max_tuple[1]    
    if algorithm == batch_job_util:
        max_tuple = (0.0,0)
        for i in range(0, len(sorted_node_id), 3):
            avg_usage = 0.0
            node_id = sorted_node_id[0].node_id
            node_machines = sorted_node_id[i:i+3]
            for machine in node_machines:
                avg_usage += machine.avg_batch_usage()
            avg_usage = avg_usage / 3
            if avg_usage > max_tuple[0]:
                max_tuple = (avg_usage, node_id)
        return max_tuple[1]
    if algorithm == service_job_scheduled_time:
        min_tuple = (1000000.0,0)
        for i in range(0, len(sorted_node_id), 3):
            avg_time = 0.0
            node_id = sorted_node_id[0].node_id
            node_machines = sorted_node_id[i:i+3]
            for machine in node_machines:
                avg_time += machine.service_job_scheduled_time()
            avg_time = avg_time / 3
            if avg_time < min_tuple[0]:
                min_tuple = (avg_time, node_id)
        return min_tuple[1]