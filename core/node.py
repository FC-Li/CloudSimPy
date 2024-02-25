from core.machine import Machine

class Node(object):
    def __init__(self, node_id, topology):
        self.id = node_id

        self.cpu_capacity = 0
        self.memory_capacity = 0
        self.disk_capacity = 0
        self.cpu = 0
        self.memory = 0
        self.disk = 0
        self.topology = topology

        self.cluster = None
        self.machines = []

    def add_machine_capacities(self, machine):
        self.cpu_capacity += machine.cpu_capacity
        self.memory_capacity += machine.memory_capacity
        self.disk_capacity += machine.disk_capacity
        self.cpu += machine.cpu_capacity
        self.memory += machine.memory_capacity
        self.disk += machine.disk_capacity

    @property
    def running_task_instances(self):
        ls = []
        for machine in self.machines:
            for task_instance in machine.task_instances:
                if task_instance.started and not task_instance.finished:
                    ls.append(task_instance)
        return ls

    @property
    def finished_task_instances(self):
        ls = []
        for machine in self.machines:
            for task_instance in machine.task_instances:
                if task_instance.finished:
                    ls.append(task_instance)
            return ls

    def attach_cluster(self, cluster):
        self.cluster = cluster

    # def attach_machine(self, machine):
    #     self.machines.append(machine)
    #     self.add_machine(machine)

    def add_machines(self, machine_configs):
        for machine_config in machine_configs:
            machine = Machine(machine_config)
            machine.attach_node(self)
            self.machines.append(machine)
            self.add_machine_capacities(machine)

    # def remove_machines(self, machines):
    #     for machine in machines:
    #         machine.dettach_node()
    #         self.machines.remove(machine)

    def delete(self):
        for running_task_instance in self.running_task_instances():
            running_task_instance.delete()
        for machine in self.machines:
            machine.dettach_node()
            self.machines.remove(machine)

    def scheduled_time(self):
        avg_time = 0.0
        running_task_instances = self.running_task_instances()
        for task_instance in running_task_instances:
            avg_time += task_instance.response_time + task_instance.running_time
        avg_time = avg_time / len(self.task_instances)
        return avg_time

    def service_job_scheduled_time(self):
        avg_time = 0.0
        running_task_instances = self.running_task_instances()
        for task_instance in running_task_instances:
            if task_instance.type == 0:
                avg_time += task_instance.response_time + task_instance.running_time
        avg_time = avg_time / len(self.task_instances)
        return avg_time

    def remaining_time(self):
        avg_time = 0.0
        running_task_instances = self.running_task_instances()
        for task_instance in running_task_instances:
            avg_time += task_instance.duration - task_instance.running_time
        avg_time = avg_time / len(self.task_instances)
        return avg_time            

    @property
    def feature(self):
        self.cpu = sum(machine.cpu for machine in self.machines)
        self.memory = sum(machine.memory for machine in self.machines)
        self.disk = sum(machine.disk for machine in self.machines)
        return [self.cpu, self.memory, self.disk]

    @property
    def capacity(self):
        return [self.cpu_capacity, self.memory_capacity, self.disk_capacity]

    @property
    def usage(self):
        self.cpu = sum(machine.cpu for machine in self.machines)
        self.memory = sum(machine.memory for machine in self.machines)
        self.disk = sum(machine.disk for machine in self.machines)
        return [self.cpu / self.cpu_capacity, self.memory / self.memory_capacity, self.disk / self.disk_capacity]

    @property
    def avg_usage(self):
        self.cpu = sum(machine.cpu for machine in self.machines)
        self.memory = sum(machine.memory for machine in self.machines)
        self.disk = sum(machine.disk for machine in self.machines)
        return ((self.cpu / self.cpu_capacity) + (self.memory / self.memory_capacity) + (self.disk / self.disk_capacity)) / 3

    @property
    def avg_batch_usage(self):
        temp_cpu = self.cpu_capacity
        temp_mem = self.memory_capacity
        temp_disk = self.disk_capacity
        running_task_instances = self.running_task_instances()
        for task_instance in running_task_instances:
            if task_instance.type == 1:
                temp_cpu -= task_instance.cpu
                temp_mem -= task_instance.memory
                temp_disk -= task_instance.disk
        return ((temp_cpu / self.cpu_capacity) + (temp_memory / self.memory_capacity) + (temp_disk / self.disk_capacity)) / 3