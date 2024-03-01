import random

def presorted_nodes(nodes, algorithm):
    if len(nodes) <= 0:
        return None
    elif len(node.running_task_instances) <= 0:
        return None
    elif algorithm == max_util:
        max_tuple = (0.0,nodes[0])
        for node in nodes:
            usage = node.usage
            if max(usage) > max_tuple[0]:
                max_tuple = (max(usage), node)
        return max_tuple[1]       
    elif algorithm == avg_util:
        max_tuple = (0.0,nodes[0])
        for node in nodes:
            avg_usage = node.avg_usage
            if avg_usage > max_tuple[0]:
                max_tuple = (avg_usage, node)
        return max_tuple[1]
    elif algorithm == scheduled_time:
        min_tuple = (1000000.0,nodes[0])
        for node in nodes:
            avg_time = 0.0
            for machine in node.machines:
                avg_time += machine.scheduled_time
            avg_time = avg_time / 3
            if avg_time < min_tuple[0]:
                min_tuple = (avg_time, node)
        return min_tuple[1]
    elif algorithm == remaining_time:
        min_tuple = (1000000.0,nodes[0])
        for node in nodes:
            avg_time = 0.0
            for machine in node.machines:
                avg_time += machine.remaining_time
            avg_time = avg_time / 3
            if avg_time < min_tuple[0]:
                min_tuple = (avg_time, node)
        return min_tuple[1]
    elif algorithm == active_workloads:
        max_tuple = (0.0,nodes[0])
        for node in nodes:
            avg_num = 0.0
            num = node.running_task_instances
            avg_num = num / 3
            if avg_num > max_tuple[0]:
                max_tuple = (avg_num, node)
        return max_tuple[1]    
    elif algorithm == batch_job_util:
        max_tuple = (0.0,nodes[0])
        for node in nodes:
            avg_usage = 0.0
            for machine in node_machines:
                avg_usage += machine.avg_batch_usage
            avg_usage = avg_usage / 3
            if avg_usage > max_tuple[0]:
                max_tuple = (avg_usage, node)
        return max_tuple[1]
    elif algorithm == service_job_scheduled_time:
        min_tuple = (1000000.0,nodes[0])
        for node in nodes:
            avg_time = 0.0
            for machine in node_machines:
                avg_time += machine.service_job_scheduled_time
            avg_time = avg_time / 3
            if avg_time < min_tuple[0]:
                min_tuple = (avg_time, node)
        return min_tuple[1]

def receiver_sorted_nodes(nodes, algorithm, workload):
    if len(nodes) <= 0:
        return None
    elif len(node.running_task_instances) == 0 or len(node.workload_accomodation(workload)) == 0:
        return None
    elif algorithm == max_util:
        min_tuple = (10000.0, nodes[0], nodes[0].machines[0]) #find node with min_util
        min_machine = nodes[0].machine[0]
        for node in nodes:
            min_util = 0.0
            list = node.workload_accomodation(workload)
            if len(list) > 0:
                usage = node.usage(list)
                if min(usage) < min_tuple[0]:
                    min_val = 10000.0
                    for machine in list:
                        metrics = machine.usage
                        if min(metrics) < min_val:
                            min_val = min(metrics)
                            min_machine = machine
                    min_tuple = (min(usage), node, machine)
            else: 
                return (None, None)
        return (min_tuple[1], min_tuple[2])   
    elif algorithm == avg_util:
        min_tuple = (100000.0, nodes[0])
        min_machine = nodes[0].machine[0]
        for node in nodes:
            min_util = 0.0
            list = node.workload_accomodation(workload)
            if len(list) > 0:
                avg_usage = node.avg_usage(list)
                if min(avg_usage) < min_tuple[0]:
                    min_val = 10000.0
                    for machine in list:
                        metrics = machine.avg_usage
                        if min(metrics) < min_val:
                            min_val = min(metrics)
                            min_machine = machine
                    min_tuple = (min(usage), node, machine)
            else: 
                return (None, None)
        return (min_tuple[1], min_tuple[2])
    elif algorithm == scheduled_time:
        min_tuple = (1000000.0, nodes[0])
        min_machine = nodes[0].machine[0]
        for node in nodes:
            avg_time = 0.0
            list = node.workload_accomodation(workload)
            if len(list) > 0:
                min_val = 10000.0
                for machine in list:
                    machine_time = machine.scheduled_time
                    avg_time += machine_time
                    if machine_time < min_val:
                        min_val = machine_time
                        min_machine = machine
                avg_time = avg_time / len(list)
                if avg_time < min_tuple[0]:
                    min_tuple = (avg_time, node, min_machine)
            else: 
                return (None, None)
        return (min_tuple[1], min_tuple[2])
    elif algorithm == remaining_time:
        min_tuple = (1000000.0, nodes[0])
        min_machine = nodes[0].machine[0]
        for node in nodes:
            avg_time = 0.0
            list = node.workload_accomodation(workload)
            if len(list) > 0:
                min_val = 10000.0
                for machine in list:
                    machine_time = machine.remaining_time
                    avg_time += machine_time
                    if machine_time < min_val:
                        min_val = machine_time
                        min_machine = machine
                avg_time = avg_time / len(list)
                if avg_time < min_tuple[0]:
                    min_tuple = (avg_time, node, min_machine)
            else: 
                return (None, None)
        return (min_tuple[1], min_tuple[2])
    elif algorithm == active_workloads:
        min_tuple = (10000000000.0, nodes[0])
        min_machine = nodes[0].machine[0]
        for node in nodes:
            total_num == 0.0
            machines = node.workload_accomodation(workload)
            if len(machines) > 0:
                min_val = 10000.0
                for machine in list:
                    machine_workloads = len(machine.running_task_instances)
                    total_num += machine_workloads
                    if machine_workloads < min_val:
                        min_val = machine_workloads
                        min_machine = machine
                avg_num = total_num / len(machines)
                if avg_num < min_tuple[0]:
                    min_tuple = (avg_num, node, min_machine)
            else: 
                return (None, None)
        return (min_tuple[1], min_tuple[2]) 
    elif algorithm == batch_job_util:
        min_tuple = (100000.0, nodes[0])
        min_machine = nodes[0].machine[0]
        for node in nodes:
            min_util = 0.0
            list = node.workload_accomodation(workload)
            if len(list) > 0:
                avg_usage = node.avg_usage(list)
                if min(avg_usage) < min_tuple[0]:
                    min_val = 10000.0
                    for machine in list:
                        metrics = machine.avg_usage
                        if (min(metrics) < min_val):
                            min_val = min(metrics)
                            min_machine = machine
                    min_tuple = (min(usage), node, machine)
            else: 
                return (None, None)
        return (min_tuple[1], min_tuple[2])
    elif algorithm == service_job_scheduled_time:
        min_tuple = (1000000.0, nodes[0])
        min_machine = nodes[0].machine[0]
        for node in nodes:
            avg_time = 0.0
            list = node.workload_accomodation(workload)
            if len(list) > 0:
                min_val = 10000.0
                for machine in list:
                    machine_time = machine.scheduled_time
                    avg_time += machine_time
                    if machine_time < min_val:
                        min_val = machine_time
                        min_machine = machine
                avg_time = avg_time / len(list)
                if (avg_time < min_tuple[0]):
                    min_tuple = (avg_time, node, min_machine)
            else: 
                return (None, None)
        return (min_tuple[1], min_tuple[2])

def presorted_workloads(node, algorithm):
    if len(node.running_task_instances) <= 0:
        return None
    elif algorithm == max_util:
        list = node.running_task_instances
        max_tuple = (0.0, list[0])
        usage = node.usage
        max_val = max(usage)
        max_index = usage.index(max_val)
        for task_instance in list:
            metric = task_instance.return_metric(max_index)
            if metric > max_tuple[0]:
                max_tuple = (metric, task_instance)
        return max_tuple[1]
    elif algorithm == avg_util:
        list = node.running_task_instances
        max_tuple = (0.0, list[0])
        for task_instance in list:
            avg_metrics = task_instance.avg_metrics
            if avg_metrics > max_tuple[0]:
                max_tuple = (avg_metrics, task_instance)
        return max_tuple[1]    
    elif algorithm == scheduled_time:
        list = node.running_task_instances
        min_tuple = (1000000.0, list[0])
        for task_instance in list:
            scheduled_time = task_instance.scheduled_time
            if scheduled_time < min_tuple[0]:
                min_tuple = (scheduled_time, task_instance)
            return min_tuple[1]
    elif algorithm == scheduled_time:
        list = node.running_task_instances
        min_tuple = (1000000.0, list[0])
        for task_instance in list:
            rem_time = task_instance.remaining_time
            if rem_time < min_tuple[0]:
                min_tuple = (rem_time, task_instance)
            return min_tuple[1]
    elif algorithm == active_workloads:
        selected_task_instance = random.choice(node.running_task_instances)
        return selected_task_instance    
    elif algorithm == batch_job_util:
        list = node.running_batch_task_instances
        max_tuple = (0.0, node.list[0])
        for task_instance in list:
            avg_metrics = task_instance.avg_metrics
            if avg_metrics > max_tuple[0]:
                max_tuple = (avg_metrics, task_instance)
        return max_tuple[1]    
    elif algorithm == service_job_scheduled_time:
        list = node.running_service_task_instances
        min_tuple = (1000000.0, list[0])
        for task_instance in list:
            rem_time = task_instance.remaining_time
            if rem_time < min_tuple[0]:
                min_tuple = (rem_time, task_instance)
            return min_tuple[1]