from playground.auxiliary import remove_delays
from playground.auxiliary.sorted_nodes import *

def extract_workloads(cluster, algorithm, num_workloads): #synartisi mono gia extraction
    machines = cluster.machines
    nodes = cluster.nodes
    algorithm = #select which algo from sorted_nodes.py
    workloads = []
    for i in range(num_workloads):
        node = sorted_nodes(nodes, algorithm)
        workload = sorted_workloads(node, algorithm)
        workload.reset()
        workload.process.interrupt()
        workloads.append(workload)
    return workloads

def reallocate_cluster_workloads(cluster, algorithm, num_workloads): #synartisi gia reall entos cluster
    machines = cluster.machines
    nodes = cluster.nodes
    algorithm = #select which algo from sorted_nodes.py
    workloads = []
    for i in range(num_workloads):
        node = presorted_nodes(nodes, algorithm)
        workload = presorted_workloads(node, algorithm)
        workload.reset()
        receiver_node, machine = receiver_sorted_nodes(nodes, algorithm, workload)
        workload.process.interrupt()
        workload.schedule(machine)
        workloads.append((workload, machine))
    return workloads

def receive_workloads(cluster, algorithm, workloads): #synartisi gia apodoxi workloads apo allo cluster
    machines = cluster.machines
    nodes = cluster.nodes
    algorithm = #select which algo from sorted_nodes.py
    for workload in workloads:
        node, machine = receiver_sorted_nodes(nodes, algorithm, workload)
        workload.schedule(machine)
    return
