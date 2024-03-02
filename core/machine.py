from enum import Enum


class MachineConfig(object):
    idx = 0

    def __init__(self, cpu_capacity, memory_capacity, disk_capacity, topology, node_id, cpu=0, memory=0, disk=0):
        self.cpu_capacity = cpu_capacity
        self.memory_capacity = memory_capacity
        self.disk_capacity = disk_capacity
        self.topology = topology
        self.node_id = node_id

        self.cpu = 0
        self.memory = 0
        self.disk = 0

        self.id = MachineConfig.idx
        MachineConfig.idx += 1


class MachineDoor(Enum):
    TASK_IN = 0
    TASK_OUT = 1
    NULL = 3


class Machine(object):
    def __init__(self, machine_config):
        self.id = machine_config.id
        self.cpu_capacity = machine_config.cpu_capacity
        self.memory_capacity = machine_config.memory_capacity
        self.disk_capacity = machine_config.disk_capacity
        self.cpu = machine_config.cpu
        self.memory = machine_config.memory
        self.disk = machine_config.disk
        self.topology = machine_config.topology
        self.node_id = machine_config.node_id

        self.cluster = None
        self.node = None
        self.task_instances = []
        self.num_waiting_instances = 0
        self.machine_door = MachineDoor.NULL

        self.anomaly = (0,0)

    def run_task_instance(self, task_instance):
        self.cpu += task_instance.cpu
        self.memory += task_instance.memory
        self.disk += task_instance.disk
        self.task_instances.append(task_instance)
        self.machine_door = MachineDoor.TASK_IN

    def stop_task_instance(self, task_instance):
        self.cpu -= task_instance.cpu
        self.memory -= task_instance.memory
        self.disk -= task_instance.disk
        self.machine_door = MachineDoor.TASK_OUT

    def restart_task_instance(self, task_instance):
        self.cpu += task_instance.cpu
        self.memory += task_instance.memory
        self.disk += task_instance.disk
        self.machine_door = MachineDoor.TASK_IN

    @property
    def running_task_instances(self):
        ls = []
        for task_instance in self.task_instances:
            if task_instance.started and not task_instance.finished:
                ls.append(task_instance)
        return ls

    @property
    def finished_task_instances(self):
        ls = []
        for task_instance in self.task_instances:
            if task_instance.finished:
                ls.append(task_instance)
        return ls

    def remove_task_instance(self, task_instance):
        if task_instance in self.task_instances:
            self.task_instances.remove(task_instance)

    # def attach(self, cluster):
    #     self.cluster = cluster

    def attach_node(self, node):
        self.node = node
    
    def dettach_node(self):
        self.node = None

    def accommodate(self, task_instance):
        return self.cpu_capacity - self.cpu >= task_instance.cpu and \
               self.memory_capacity - self.memory >= task_instance.memory and \
               self.disk_capacity - self.disk >= task_instance.disk

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
        return [self.cpu, self.memory, self.disk]

    @property
    def capacity(self):
        return [self.cpu_capacity, self.memory_capacity, self.disk_capacity]

    @property
    def usage(self):
        return [self.cpu / self.cpu_capacity, self.memory / self.memory_capacity, self.disk / self.disk_capacity]

    @property
    def avg_usage(self):
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

    @property
    def state(self):
        return {
            'id': self.id,
            'cpu_capacity': self.cpu_capacity,
            'memory_capacity': self.memory_capacity,
            'disk_capacity': self.disk_capacity,
            'cpu': self.cpu / self.cpu_capacity,
            'memory': self.memory / self.memory_capacity,
            'disk': self.disk / self.disk_capacity,
            'running_task_instances': len(self.running_task_instances),
            'finished_task_instances': len(self.finished_task_instances)
        }

    def __eq__(self, other):
        return isinstance(other, Machine) and other.id == self.id
