import random

from playground.auxiliary import remove_delays
from playground.auxiliary.sorted_nodes import *

def extract_workloads(cluster, algorithm, num_workloads): #synartisi mono gia extraction
    machines = cluster.machines
    nodes = cluster.nodes
    algorithm = algorithm #select which algo from sorted_nodes.py
    workloads = []
    for i in range(num_workloads):
        node = sorted_nodes(nodes, algorithm)
        workload = sorted_workloads(node, algorithm)
        workload.reset_instance()
        workload.process.interrupt()
        workloads.append(workload)
    return workloads

def reallocate_cluster_workloads(cluster, algorithm, num_workloads): #synartisi gia reall entos cluster
    machines = cluster.machines
    nodes = cluster.nodes
    algorithm = algorithm #select which algo from sorted_nodes.py
    workloads = []
    for i in range(num_workloads):
        node = presorted_nodes(nodes, algorithm)
        workload = presorted_workloads(node, algorithm)
        workload.reset_instance()
        receiver_node, machine = receiver_sorted_nodes(nodes, algorithm, workload)
        workload.process.interrupt()
        workload.schedule(machine)
        workloads.append((workload, machine))
    return workloads

def receive_workloads(cluster, algorithm, workloads): #synartisi gia apodoxi workloads apo allo cluster
    machines = cluster.machines
    nodes = cluster.nodes
    algorithm = algorithm #select which algo from sorted_nodes.py
    for workload in workloads:
        node, machine = receiver_sorted_nodes(nodes, algorithm, workload)
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


