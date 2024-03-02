import random

from core.machine import Machine
from core.machine import MachineConfig
from core.node import Node
from playground.auxiliary.find_missing_item import find_first_missing_integer


class Cluster(object):
    def __init__(self, level=None):
        # self.machines = []
        self.nodes = []
        self.jobs = []
        self.level = level  # Optional: Identify the cluster level or type
        self.child_clusters = [] if level is None else None  # Central cluster has child clusters

    @property
    def unfinished_jobs(self):
        ls = []
        if self.child_clusters is not None:
            for child in self.child_clusters:
                for job in child.jobs:
                    if not job.finished:
                        ls.append(job)
        else:
            for job in self.jobs:
                if not job.finished:
                    ls.append(job)
        return ls

    @property
    def unfinished_tasks(self):
        ls = []
        for job in self.unfinished_jobs:
            ls.extend(job.unfinished_tasks)
        return ls

    @property
    def ready_unfinished_tasks(self):
        ls = []
        for job in self.jobs:
            ls.extend(job.ready_unfinished_tasks)
        return ls

    @property
    def tasks_which_has_waiting_instance(self):
        ls = []
        for job in self.jobs:
            ls.extend(job.tasks_which_has_waiting_instance)
        return ls

    @property
    def ready_tasks_which_has_waiting_instance(self):
        ls = []
        for job in self.jobs:
            ls.extend(job.ready_tasks_which_has_waiting_instance)
        return ls

    @property
    def finished_jobs(self):
        ls = []
        for job in self.jobs:
            if job.finished:
                ls.append(job)
        return ls

    @property
    def finished_tasks(self):
        ls = []
        for job in self.jobs:
            ls.extend(job.finished_tasks)
        return ls

    @property
    def running_task_instances(self):
        if self.child_clusters is not None:
            task_instances = []
            for child in self.child_clusters:
                task_instances.extend(child.running_task_instances)
            return task_instances
        else:
            task_instances = []
            for node in self.nodes:
                task_instances.extend(node.running_task_instances)
            return task_instances

    @property
    def waiting_task_instances(self):
        if self.child_clusters is not None:
            task_instances = []
            for child in self.child_clusters:
                task_instances.extend(child.waiting_task_instances)
            return task_instances
        else:
            task_instances = []
            for node in self.nodes:
                task_instances.extend(node.waiting_task_instances)
            return task_instances

    @property
    def metrics_unstarted_instances(self):
        if self.child_clusters is not None:
            ls = []
            for child in self.child_clusters:
                ls.extend(child.metrics_unstarted_instances)
            return ls
        else:
            ls = []
            cluster_sum = [0,0,0]
            for node in child.nodes:
                node_sum = node.metrics_unstarted_instances
                cluster_sum[0] += node_sum[0]
                cluster_sum[1] += node_sum[1]
                cluster_sum[2] += node_sum[2]
            ls.append(cluster_sum)
            return ls

    def add_nodes(self, nodes):
        if self.child_clusters is not None:
            for node in nodes:
                target_cluster = node.topology
                self.child_clusters[target_cluster].add_nodes(node)
        else:
            for node in nodes:
                self.nodes.append(node)
                node.attach_cluster(self)

    def create_nodes(self, target_cluster, num):
        if self.child_clusters is not None:
            for i in range(num-1):
                node_id = find_first_missing_integer()
                machine_configs = [MachineConfig(2, 1, 1, target_cluster, node_id) for _ in range(3)]
                Node(node_id, target_cluster).add_machines(machine_configs)
                self.child_clusters[target_cluster].add_nodes(Node(node_id, target_cluster))

    def remove_nodes(self, nodes):
        for node in nodes:
            self.nodes.remove(node)
            node.delete()

    def add_job(self, job):
        if self.child_clusters is not None:
            # Central cluster randomly chooses a child cluster for the job
            random.choice(self.child_clusters).add_job(job) # i can add any algorithm i want
        else:
            self.jobs.append(job)

    @property
    def cpu(self):
        if self.child_clusters is not None:
            ls = []
            for child in self.child_clusters:
                ls.append(child.cpu)
            return ls
        else:
            return sum([machine.cpu for node in self.nodes for machine in node.machines])

    @property
    def memory(self):
        if self.child_clusters is not None:
            ls = []
            for child in self.child_clusters:
                ls.append(child.memory)
            return ls
        else:
            return sum([machine.memory for node in self.nodes for machine in node.machines])
        

    @property
    def disk(self):
        if self.child_clusters is not None:
            ls = []
            for child in self.child_clusters:
                ls.append(child.disk)
            return ls
        else:
            return sum([machine.cpu for node in self.nodes for machine in node.machines])
        

    @property
    def cpu_capacity(self):
        if self.child_clusters is not None:
            ls = []
            for child in self.child_clusters:
                ls.append(child.cpu_capacity)
            return ls
        else:
            return sum(machine.cpu_capacity for node in self.nodes for machine in node.machines)
        

    @property
    def memory_capacity(self):
        if self.child_clusters is not None:
            ls = []
            for child in self.child_clusters:
                ls.append(child.memory_capacity)
            return ls
        else:
            return sum(machine.memory_capacity for node in self.nodes for machine in node.machines)
        

    @property
    def disk_capacity(self):
        if self.child_clusters is not None:
            ls = []
            for child in self.child_clusters:
                ls.append(child.disk_capacity)
            return ls
        else:
            return sum(machine.disk_capacity for node in self.nodes for machine in node.machines)

    @property
    def usage(self):
        if self.child_clusters is not None:
            ls = []
            for child in self.child_clusters:
                ls.append([child.cpu, child.memory, child.disk])
            return ls
        else:
            return [self.cpu, self.memory, self.disk]

    @property
    def avg_usage(self):
        if self.child_clusters is not None:
            sum = 0
            for child in self.child_clusters:
                cl_sum = child.avg_usage
                sum += cl_sum
            sum = sum / len(self.child_clusters)
            return sum
        else:
            sum = 0 
            for node in self.nodes:
                sum += node.avg_usage
            sum = sum / len(self.nodes)
            return sum

    @property
    def response_times(self):
        if self.child_clusters is not None:
        batch_times = []
        service_times = []
            for child in self.child_clusters:
                l1, l2 = child.response_time_tuples
                service_times.extend(l1)
                batch_times.extend(l2)
            return service_times, batch_times
        else:
            batch_times = []
            service_times = []
            for node in child.nodes:
                l1, l2 = node.all_response_time_tuples
                service_times.extend(l1)
                batch_times.extend(l2)
            return service_times, batch_times
    
    @property
    def capacities(self):
        if self.child_clusters is not None:
            ls = []
            for child in self.child_clusters:
                ls.append([child.cpu_capacity, child.memory_capacity, child.disk_capacity])
            return ls
        else:
            return [self.cpu_capacity, self.memory_capacity, self.disk_capacity]

    @property
    def anomalous_usage(self):
        if self.child_clusters is not None:
            ls = []
            for child in self.child_clusters:
                cnt = child.anomalous_usage
                ls.append(cnt)
            return ls
        else:
            cnt = 0
            for node in self.nodes:
                for machine in node.machines:
                    usage = machine.usage
                    if any(val > 1 for val in usage):
                        cnt += 1
            return cnt

    @property
    def response_time(self):
        if self.child_clusters is not None:
            ls = []
            for child in self.child_clusters:
                avg = 0
                for node in child.nodes:
                    avg += node.response_time
                avg = avg / len(child.nodes)
                ls.append(avg)
            return ls
        else:
            ls = []
            avg = 0
            for node in self.nodes:
                avg += node.response_time
            avg = avg / len(child.nodes)
            ls.append(avg)
            return ls

    # @property
    # def state(self):
    #     return {
    #         'arrived_jobs': len(self.jobs),
    #         'unfinished_jobs': len(self.unfinished_jobs),
    #         'finished_jobs': len(self.finished_jobs),
    #         'unfinished_tasks': len(self.unfinished_tasks),
    #         'finished_tasks': len(self.finished_tasks),
    #         'running_task_instances': len(self.running_task_instances),
    #         'machine_states': [machine.state for machine in self.machines],
    #         'cpu': self.cpu / self.cpu_capacity,
    #         'memory': self.memory / self.memory_capacity,
    #         'disk': self.disk / self.disk_capacity,
    #     }

    # def add_machines(self, machine_configs):
    #     if self.child_clusters is not None:
    #         for machine_config in machine_configs:
    #             machine = Machine(machine_config)
    #             target_cluster = machine.topology
    #             self.child_clusters[target_cluster].add_machine(machine)
    #     else:
    #         for machine_config in machine_configs:
    #             machine = Machine(machine_config)
    #             self.machines.append(machine)
    #             machine.attach(self)

    # def add_machine(self, machine):
    #     self.machines.append(machine)
    #     machine.attach(self)
        
    # def remove_machines(self, machine_configs):
    #     if self.child_clusters is not None:
    #         for machine_config in machine_configs:
    #             machine = Machine(machine_config)
    #             target_cluster = machine.topology
    #             if machine in self.child_clusters[target_cluster].machines:
    #                 self.child_clusters[target_cluster].remove(machine)
