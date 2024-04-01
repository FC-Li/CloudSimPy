import random

from playground.auxiliary.sorted_nodes import *

def extract_jobs(cluster, algorithm, num_jobs): #synartisi mono gia extraction
    machines = cluster.cluster_machines
    jobs = cluster.jobs
    selected_jobs = []
    if len(jobs) == 0:
        return None
    if len(cluster.unfinished_jobs) == 0:
        return None
    algorithm = algorithm #select which algo from sorted_nodes.py
    if num_jobs > len(jobs):
        num_jobs = len(jobs)
    for i in range(num_jobs):
        job = presorted_jobs(cluster, algorithm)
        for task_instance in job.task_instances:
            started = task_instance.started
            finished = task_instance.finished
            if task_instance.started:
                task_instance.reset_instance()
            if (started and not finished):
                task_instance.process.interrupt()
        cluster.jobs.remove(job)
        selected_jobs.append(job)
    return selected_jobs

def reallocate_cluster_workloads(cluster, algorithm, num_workloads): #synartisi gia reall entos cluster
    machines = cluster.cluster_machines
    nodes = cluster.nodes
    if len(nodes)== 0:
        return None
    algorithm = algorithm #select which algo from sorted_nodes.py
    workloads = []
    for i in range(num_workloads):
        node = presorted_nodes(cluster, algorithm)
        workload = presorted_workloads(node, algorithm)
        if workload == None:
            continue
        receiver_node, machine = receiver_sorted_nodes(nodes, algorithm, workload)
        if machine == None:
            continue
        workload.reset_instance()
        workload.process.interrupt()
        workload.schedule(machine)
        workloads.append((workload, machine))
    return workloads

def receive_jobs(cluster, algorithm, jobs): #synartisi gia apodoxi workloads apo allo cluster
    machines = cluster.cluster_machines
    nodes = cluster.nodes
    workloads = []
    if jobs == None:
        return
    for job in jobs:
        cluster.jobs.append(job)
        workloads.extend(job.task_instances)
    if len(nodes) == 0:
        return 
    algorithm = algorithm #select which algo from sorted_nodes.py
    for workload in workloads:
        node, machine = receiver_sorted_nodes(nodes, algorithm, workload)
        if machine != None:
            workload.schedule(machine)
    return

def redirect_workload(machines):
    for machine in machines:
        task_instance = random.choice(machine.waiting_task_instances)
        for other_machine in machine.node.cluster.cluster_machines:
            if other_machine.accommodate(task_instance):
                print('i am task instance %f of task %f of job %f and i will be interrupted with remaining time %f' \
                % (task_instance.task_instance_index, task_instance.task.task_index, task_instance.task.job.id, \
                task_instance.duration - task_instance.running_time))
                task_instance.reset_instance()
                task_instance.process.interrupt()
                task_instance.schedule(other_machine)
                print('i am task instance %f of task %f and i am moving from machine %f to machine %f' \
                % (task_instance.task_instance_index, task_instance.task.task_index, machine.id, other_machine.id))
                break


