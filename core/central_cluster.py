import random

from core.machine import Machine
from core.machine import MachineConfig
from core.node import Node
from playground.auxiliary.find_missing_item import find_first_missing_integer


class Cluster(object):
    def __init__(self, level=None, capacity=None):
        # self.machines = []
        self.nodes = []
        self.jobs = []
        self.node_capacity = capacity
        self.level = level  # Optional: Identify the cluster level or type
        self.child_clusters = [] if level is None else None  # Central cluster has child clusters
        self.deleted_nodes_info = [[],[]]

    @property
    def unfinished_jobs(self):
        ls = []
        if self.child_clusters is not None:
            for child in self.child_clusters:
                ls.extend(child.unfinished_jobs)
        else:
            ls = []
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
    def running_unfinished_instances(self):
        ls = []
        for task in self.unfinished_tasks:
            ls.extend(task.running_unfinished_task_instances)
        return ls
    
    @property
    def unfinished_instances(self):
        if self.child_clusters is not None:
            instances = []
            for child in self.child_clusters:
                instances.append(child.unfinished_instances)
            return instances
        else:
            ls = []
            for task in self.unfinished_tasks:
                ls.extend(task.unfinished_task_instances)
            return len(ls)

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
        if self.child_clusters is not None:
            tasks = []
            for child in self.child_clusters:
                tasks.extend(child.ready_tasks_which_has_waiting_instance)
            return jobs
        else:
            ls = []
            for job in self.jobs:
                ls.extend(job.ready_tasks_which_has_waiting_instance)
            return ls

    @property
    def finished_jobs(self):
        if self.child_clusters is not None:
            jobs = []
            for child in self.child_clusters:
                jobs.extend(child.finished_jobs)
            return jobs
        else:
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
    def finished_task_instances(self):
        if self.child_clusters is not None:
            cnt = 0
            for child in self.child_clusters:
                cnt += child.finished_task_instances
            return cnt
        else:
            cnt = 0
            for job in self.jobs:
                for task in job.tasks:
                    for task_instance in task.task_instances:
                        if task_instance.finished:
                            cnt += 1
            return cnt

    @property
    def started_task_instances(self):
        if self.child_clusters is not None:
            task_instances = []
            for child in self.child_clusters:
                task_instances.extend(child.started_task_instances)
            return task_instances
        else:
            task_instances = []
            for node in self.nodes:
                task_instances.extend(node.unfinished_task_instances)
            return task_instances
    
    @property
    def separate_len_started_task_instances(self):
        if self.child_clusters is not None:
            task_instances = []
            for child in self.child_clusters:
                task_instances.append(len(child.started_task_instances))
            return task_instances

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
                task_instances.extend(node.running_task_instances())
            return task_instances

    @property
    def separate_len_running_task_instances(self):
        if self.child_clusters is not None:
            task_instances = []
            for child in self.child_clusters:
                task_instances.append(len(child.running_task_instances))
            return task_instances

    @property
    def service_running_task_instances(self):
        if self.child_clusters is not None:
            task_instances = []
            for child in self.child_clusters:
                task_instances.append(len(child.service_running_task_instances))
            return task_instances
        else:
            task_instances = []
            for node in self.nodes:
                task_instances.extend(node.unfinished_service_task_instances)
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
                task_instances.extend(node.waiting_task_instances())
            return task_instances
    
    @property
    def unscheduled_task_instances(self):
        if self.child_clusters is not None:
            task_instances = []
            for child in self.child_clusters:
                task_instances.extend(child.unscheduled_task_instances)
            return task_instances
        else:
            task_instances = []
            for job in self.jobs:
                for task in job.tasks:
                    task_instances.extend(task.unscheduled_task_instances)
            return task_instances

    @property
    def separate_len_unscheduled_task_instances(self):
        if self.child_clusters is not None:
            task_instances = []
            for child in self.child_clusters:
                task_instances.append(len(child.unscheduled_task_instances))
            return task_instances
            
    @property
    def separate_len_0_1_unscheduled_task_instances(self):
        if self.child_clusters is not None:
            task_instances = []
            for child in self.child_clusters:
                if len(child.unscheduled_task_instances) > 0:
                    task_instances.append(1)
                else:
                    task_instances.append(0)
            return task_instances

    @property
    def non_waiting_instances(self):
        if self.child_clusters is not None:
            task_instances = []
            for child in self.child_clusters:
                task_instances.extend(child.non_waiting_instances)
            return task_instances
        else:
            task_instances = []
            for node in self.nodes:
                task_instances.extend(node.non_waiting_instances())
            return task_instances

    @property
    def not_started_task_instances(self):
        if self.child_clusters is not None:
            task_instances = []
            for child in self.child_clusters:
                task_instances.extend(child.not_started_task_instances)
            return task_instances
        else:
            task_instances = []
            for job in self.jobs:
                for task in job.tasks:
                    task_instances.extend(task.unscheduled_task_instances)
            return task_instances
    
    @property
    def separate_len_unscheduled_task_instances(self):
        if self.child_clusters is not None:
            task_instances = []
            for child in self.child_clusters:
                task_instances.append(len(child.not_started_task_instances))
            return task_instances

    @property
    def unfinished_task_instances(self):
        if self.child_clusters is not None:
            task_instances = []
            for child in self.child_clusters:
                task_instances.extend(child.unfinished_task_instances)
            return task_instances
        else:
            task_instances = []
            for node in self.nodes:
                task_instances.extend(node.unfinished_task_instances)
            return task_instances 

    @property
    def finished_type_task_instances(self):
        if self.child_clusters is not None:
            service_percentage = []
            batch_percentage = []
            for child in self.child_clusters:
                ls = child.finished_type_task_instances
                service_percentage.append(ls[0])
                batch_percentage.append(ls[1])
            return [service_percentage, batch_percentage]
        else:
            service_instances = []
            batch_instances = []
            for node in self.nodes:
                ls = node.finished_type_task_instances
                service_instances.extend(ls[0])
                batch_instances.extend(ls[1])
            service_instances.extend(self.deleted_nodes_info[0])
            batch_instances.extend(self.deleted_nodes_info[1])
            overall_len = len(service_instances) + len(batch_instances)
            if overall_len == 0:
                return [0,0]
            return [len(service_instances)/ overall_len, len(batch_instances)/ overall_len]     
    
    @property
    def finished_response_times(self):
        if self.child_clusters is not None:
            service_instances = 0
            batch_instances = 0
            service_len = 0
            batch_len = 0
            for child in self.child_clusters:
                ls = child.finished_response_times
                service_instances += ls[0][0]
                service_len += ls[0][1]
                batch_instances += ls[1][0]
                batch_len += ls[1][1]
            if batch_len == 0:
                batch_instances = 0
                batch_len = 1
            if service_len == 0:
                service_instances = 0
                service_len = 1
            return [service_instances / service_len, batch_instances / batch_len]
        else:
            service_instances = 0
            batch_instances = 0
            service_len = 0
            batch_len = 0
            for node in self.nodes:
                ls = node.finished_response_times()
                service_instances += ls[0][0]
                service_len += ls[0][1]
                batch_instances += ls[1][0]
                batch_len += ls[1][1]
            return [[service_instances, service_len], [batch_instances, batch_len]] 
        
    @property
    def overall_finished_response_times(self):
        if self.child_clusters is not None:
            instances = 0
            len_instances = 0
            for child in self.child_clusters:
                ls = child.overall_finished_response_times
                instances += ls[0]
                len_instances += ls[1]
            if len_instances == 0:
                instances = 0
                len_instances = 1
            return [instances / len_instances]
        else:
            instances = 0
            len_instances = 0
            for node in self.nodes:
                ls = node.overall_finished_response_times()
                instances += ls[0]
                len_instances += ls[1]
            return [instances, len_instances] 
    @property
    def finished_type_response_times(self):
        if self.child_clusters is not None:
            service_instances = []
            batch_instances = []
            for child in self.child_clusters:
                ls = child.finished_type_response_times
                service_instances.extend(ls[0])
                batch_instances.extend(ls[1])
            return service_instances, batch_instances
        else:
            service_instances = []
            batch_instances = []
            for node in self.nodes:
                ls = node.finished_type_task_instances
                service_instances.extend(ls[0])
                batch_instances.extend(ls[1])
            return [service_instances, batch_instances] 
    
    @property
    def deleted_nodes_times(self):
        if self.child_clusters is not None:
            ls = [[],[]]
            for child in self.child_clusters:
                ls[0].extend(child.deleted_nodes_times[0])
                ls[1].extend(child.deleted_nodes_times[1])
            return ls
        else:
            return self.deleted_nodes_info

    @property
    def machines_only_waiting_instances(self):
        if self.child_clusters is not None:
            machines = []
            for child in self.child_clusters:
                machines.extend(child.machines_only_waiting_instances)
            return machines
        else:
            machines = []
            for node in self.nodes:
                for machine in node.machines:
                    if (machine.running_task_instances == [] and \
                    machine.unstarted_task_instances == [] and machine.waiting_task_instances != []):
                        machines.append(machine)
            return machines

    @property
    def cluster_machines(self):
        if self.child_clusters is not None:
            machines = []
            for child in self.child_clusters:
                machines.extend(child.cluster_machines)
            return machines
        else:
            machines = []
            for node in self.nodes:
                machines.extend(node.machines)
            return machines   

    @property
    def len_all_task_instances(self):
        task_instances = []
        task_instances.extend(self.running_task_instances)
        task_instances.extend(self.waiting_task_instances)
        task_instances.extend(self.unscheduled_task_instances)
        return len(task_instances)

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
            task_instances = []
            for job in self.jobs:
                for task in job.tasks:
                    for task_instance in task.unscheduled_task_instances:
                        cluster_sum[0] += task_instance.cpu
                        cluster_sum[1] += task_instance.memory
                        cluster_sum[2] += task_instance.disk
            ls.append(cluster_sum[:2])
            return ls

    def add_nodes(self, nodes):
        if self.child_clusters is not None:
            for node in nodes:
                target_cluster = node.topology
                self.child_clusters[target_cluster].add_nodes([node])
        else:
            for node in nodes:
                self.nodes.append(node)
                node.attach_cluster(self)

    def create_nodes(self, target_cluster, num):
        if self.child_clusters is not None:
            if num > (self.child_clusters[target_cluster].node_capacity - \
            len(self.child_clusters[target_cluster].nodes)):
                num = (self.child_clusters[target_cluster].node_capacity - \
                len(self.child_clusters[target_cluster].nodes))
            for i in range(int(num)):
                node_id = find_first_missing_integer(self.nodes)
                machine_configs = [MachineConfig(3, 3, 1, target_cluster, node_id) for _ in range(3)]
                node = Node(node_id, target_cluster)
                node.add_machines(machine_configs)
                self.child_clusters[target_cluster].add_nodes([node])

    def remove_nodes(self, target_cluster, num):
        if self.child_clusters is not None:
            for i in range(num):
                if len(self.child_clusters[target_cluster].nodes) > 1:
                    node = random.choice(self.child_clusters[target_cluster].nodes)
                    ls = node.finished_type_task_instances
                    self.child_clusters[target_cluster].deleted_nodes_info[0].extend(ls[0])
                    self.child_clusters[target_cluster].deleted_nodes_info[1].extend(ls[1])
                    self.child_clusters[target_cluster].nodes.remove(node)
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
            return sum([machine.disk for node in self.nodes for machine in node.machines])
        

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
                ls.append(child.usage)
            return ls
        else:
            if self.capacities[0] == 0:
                return [0, 0]
            return [self.cpu / self.capacities[0], self.memory / self.capacities[1]]
            # return [self.cpu / self.capacities[0], self.memory / self.capacities[1], \
            # self.disk / self.capacities[2]]

    @property
    def average_metrics_usage(self):
        if self.child_clusters is not None:
            ls = []
            for child in self.child_clusters:
                ls.append(child.usage)
            return ls
        else:
            ls = [0,0,0]
            num = len(self.nodes)
            if num > 0:
                for node in self.nodes:
                    metrics = node.usage()
                    ls[0] += metrics[0]
                    ls[1] += metrics[1]
                    ls[2] += metrics[2]
                # Divide each element by the constant
                ls = [element / num for element in ls]
            return ls

    @property
    def avg_usage(self):
        if self.child_clusters is not None:
            sum = 0
            num = 0
            for child in self.child_clusters:
                cl_sum, cl_len = child.avg_usage
                if cl_len == 0:
                    continue
                sum += cl_sum
                num += cl_len
            sum = sum / num
            return sum
        else:
            sum = 0 
            num = 0
            for node in self.nodes:
                sum += node.avg_usage()
            num += len(self.nodes)
            return sum, num

    @property
    def response_times(self):
        if self.child_clusters is not None:
            batch_times = []
            service_times = []
            for child in self.child_clusters:
                l1, l2 = child.response_times
                service_times.extend(l1)
                batch_times.extend(l2)
            return service_times, batch_times
        else:
            cnt = 0
            batch_times = []
            service_times = []
            for job in self.jobs:
                for task in job.tasks:
                    for task_instance in task.task_instances:
                        if task_instance.finished == False:
                            if task_instance.started == False:
                                task_instance.response_time = task_instance.env.now - \
                                task_instance.task.task_config.submit_time + \
                                task_instance.config.before_0_response_time
                            if (task_instance.task.job.type == 2):
                                service_times.append(task_instance)
                            elif (task_instance.task.job.type == 1):
                                batch_times.append(task_instance)
            # sum = len(batch_times) + len(service_times)
            return service_times, batch_times

    @property
    def transmit_delays(self):
        if self.child_clusters is not None:
            ls = []
            for child in self.child_clusters:
                ls.append(child.transmit_delays)
            return ls
        else:
            cnt = 0
            for job in self.jobs:
                for task in job.unfinished_tasks:
                    for task_instance in task.unfinished_task_instances:
                        if (task_instance.task.job.type == 2):
                            cnt += 1
            return cnt
    
    @property
    def capacities(self):
        if self.child_clusters is not None:
            ls = []
            for child in self.child_clusters:
                ls.append([child.cpu_capacity, child.memory_capacity])
                # ls.append([child.cpu_capacity, child.memory_capacity, child.disk_capacity])
            return ls
        else:
            return [self.cpu_capacity, self.memory_capacity]
            # return [self.cpu_capacity, self.memory_capacity, self.disk_capacity]
        
    # @property
    # def active_nodes(self):
    #     if self.child_clusters is not None:
    #         ls = []
    #         for child in self.child_clusters:
    #             ls.append(child.active_nodes)
    #         return ls
    #     else:
    #         return len(self.nodes)

    # @property
    # def node_capacities(self):
    #     if self.child_clusters is not None:
    #         ls = []
    #         for child in self.child_clusters:
    #             ls.append(child.node_capacities)
    #         return ls
    #     else:
    #         return self.node_capacity
    
    @property
    def nodes_num_usage(self):
        if self.child_clusters is not None:
            ls = []
            for child in self.child_clusters:
                ls.append(child.nodes_num_usage)
            return ls
        else:
            if len(self.nodes) == 1:
                return 0
            elif (len(self.nodes) / self.node_capacity)< 0.2:
                return 0.1
            elif (len(self.nodes) / self.node_capacity)< 0.4:
                return 0.3
            elif (len(self.nodes) / self.node_capacity)< 0.7:
                return 0.5
            elif (len(self.nodes) / self.node_capacity)< 0.9:
                return 0.8
            # elif len(self.nodes) != self.node_capacity:
            #     return 0.5
            else:
                return 1
            # return (len(self.nodes)/ self.node_capacity)

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
    def anomaly_update(self):
        if self.child_clusters is not None:
            ls = []
            for child in self.child_clusters:
                ls.extend(child.anomaly_update)
            return ls
        else:
            ls = []
            for node in self.nodes:
                for machine in node.machines:
                    usage = machine.usage
                    machine.anomaly[0] = machine.anomaly[1]
                    if any(val > 1 for val in usage):
                        machine.anomaly[1] = 1
                    else:
                        machine.anomaly[1] = 0
                    ls.append(machine.anomaly)
            return ls
    
    @property
    def continuous_anomaly(self):
        if self.child_clusters is not None:
            ls = []
            cnt = 0
            overall_len = 0
            for child in self.child_clusters:
                cnt += child.continuous_anomaly[0]
                overall_len += child.continuous_anomaly[1]
                ls.append(cnt / overall_len)
            return ls
        else:
            cnt = 0
            for node in self.nodes:
                for machine in node.machines:
                    usage = machine.usage
                    machine.anomaly[0] = machine.anomaly[1]
                    if any(val > 1 for val in usage):
                        machine.anomaly[1] = 1
                    else:
                        machine.anomaly[1] = 0
                    if (machine.anomaly[0] == 1 and machine.anomaly[1] == 1):
                        cnt += 1
            return [cnt, len(node.machines)]

    @property
    def overall_separate_response_times(self):
        if self.child_clusters is not None:
            ls = []
            for child in self.child_clusters:
                avg, cnt = child.overall_response_time
                if (cnt == 0):
                    ls.append(0)
                else:
                    ls.append(avg / cnt)
            return ls
        else:
            cnt = 0
            avg = 0
            for job in self.jobs:
                for task_instance in job.task_instances:
                    avg += task_instance.response_time 
                    cnt += 1
            for instance in self.deleted_nodes_info[0]:
                avg += instance.response_time
                cnt += 1
            for instance in self.deleted_nodes_info[1]:
                avg += instance.response_time
                cnt += 1   
            return avg, cnt
    
    @property
    def overall_response_time(self):
        if self.child_clusters is not None:
            avg = cnt = 0
            for child in self.child_clusters:
                avg += child.overall_response_time[0]
                cnt += child.overall_response_time[1]
            if (cnt == 0):
                return 0
            else:
                return avg / cnt
        else:
            cnt = 0
            avg = 0
            for job in self.jobs:
                for task_instance in job.task_instances:
                    avg += task_instance.response_time 
                    cnt += 1
            for instance in self.deleted_nodes_info[0]:
                avg += instance.response_time
                cnt += 1
            for instance in self.deleted_nodes_info[1]:
                avg += instance.response_time
                cnt += 1   
            return [avg, cnt]
    
    @property
    def average_kwh_cost(self):
        if self.child_clusters is not None:
            cost = 0
            for child in self.child_clusters:
                cost += child.average_kwh_cost
            return cost
        else:
            cost = 0
            for node in self.nodes:
                for machine in node.machines:
                    cost += 1.5 * 0.2327 #kwh * price of kwh
            return cost

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
