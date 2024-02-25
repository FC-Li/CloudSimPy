import random

from core.machine import Machine


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
        task_instances = []
        for node in self.nodes:
            for machine in node.machines:
                task_instances.extend(machine.running_task_instances)
        return task_instances

    def add_nodes(self, nodes):
        if self.child_clusters is not None:
            for node in nodes:
                target_cluster = node.topology
                self.child_clusters[target_cluster].add_node(node)
        else:
            for node in nodes:
                self.nodes.append(node)
                node.attach_cluster(self)
    
    def add_node(self, node):
        self.nodes.append(node)
        node.attach_cluster(self)

    def remove_node(self, node):
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
        return sum([machine.cpu for node in self.nodes for machine in node.machines])

    @property
    def memory(self):
        return sum([machine.memory for node in self.nodes for machine in node.machines])

    @property
    def disk(self):
        return sum([machine.disk for node in self.nodes for machine in node.machines])

    @property
    def cpu_capacity(self):
        return sum(machine.cpu_capacity for node in self.nodes for machine in node.machines)

    @property
    def memory_capacity(self):
        return sum(machine.memory_capacity for node in self.nodes for machine in node.machines)

    @property
    def disk_capacity(self):
        return sum(machine.disk_capacity for node in self.nodes for machine in node.machines)

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