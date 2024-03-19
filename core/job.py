import simpy

from core.config import *

class Task(object):
    def __init__(self, env, job, task_config):
        self.env = env
        self.job = job
        self.task_index = task_config.task_index
        self.task_config = task_config
        self.response_time = task_config.response_time
        self._ready = False
        self._parents = None

        self.task_instances = []
        task_instance_config = TaskInstanceConfig(task_config)
        for task_instance_index in range(int(self.task_config.instances_number)):
            self.task_instances.append(TaskInstance(self.env, self, task_instance_index, task_instance_config))
        self.next_instance_pointer = 0

    @property
    def id(self):
        return str(self.job.id) + '-' + str(self.task_index)

    @property
    def parents(self):
        if self._parents is None:
            if self.task_config.parent_indices is None:
                self._parents = []
            self._parents = []
            for parent_index in self.task_config.parent_indices:
                self._parents.append(self.job.tasks_map[parent_index])
        return self._parents

    @property
    def ready(self):
        if not self._ready:
            for p in self.parents:
                if not p.finished:
                    return False
            self._ready = True
        return self._ready

    @property
    def running_task_instances(self):
        ls = []
        for task_instance in self.task_instances:
            if task_instance.started and not task_instance.finished:
                ls.append(task_instance)
        return ls

    @property
    def unfinished_task_instances(self):
        ls = []
        for task_instance in self.task_instances:
            if ((task_instance.started and not task_instance.finished) \
            or task_instance.waiting):
                ls.append(task_instance)
        return ls

    @property
    def finished_task_instances(self):
        ls = []
        for task_instance in self.task_instances:
            if task_instance.finished:
                ls.append(task_instance)
        return ls

    @property
    def unscheduled_task_instances(self):
        ls = []
        for task_instance in self.task_instances:
            if not task_instance.started:
                ls.append(task_instance)
        return ls   

    # the most heavy
    def start_task_instance(self, task_instance_index, machine):
        self.task_instances[task_instance_index].schedule(machine)
        # self.task_instances[self.next_instance_pointer].schedule(machine)
        # self.next_instance_pointer += 1

    # when the task instance remains in the same cluster // when it is a batch job
    # def reset_task_instance(self, task_instance_index, task_instance_config):
    #     # self.task_config.instances_number = str(int(self.task_config.instances_number) + 1)
    #     self.task_instances.append(TaskInstance(self.env, self, task_instance_index, task_instance_config))

    def refresh_response_time(self, response_time):
        self.response_time = response_time
        for i in range(int(self.next_instance_pointer), int(self.task_config.instances_number)):
            self.task_instances[i].passive_refresh_response_time(response_time)
 
    @property
    def running_time(self):
        max_inst = 0.0
        for task_instance in self.task_instances:
            if (task_instance.running_time + task_instance.running_time) > max_inst:
                max_inst = task_instance.running_time + task_instance.running_time
        return max_inst

    @property
    def started(self):
        for task_instance in self.task_instances:
            if task_instance.started:
                return True
        return False

    # @property
    # def waiting_task_instances_number(self):
    #     return self.task_config.instances_number - self.next_instance_pointer

    @property
    def has_waiting_task_instances(self):
        if len(self.unscheduled_task_instances) != 0:
            return True
        return False

    @property
    def finished(self):
        """
        A task is finished only if it has no waiting task instances and no running task instances.
        :return: bool
        """
        ls = []
        ls.extend(self.unfinished_task_instances)
        ls.extend(self.unscheduled_task_instances)
        if len(ls) != 0:
            return False
        return True

    @property
    def started_timestamp(self):
        t = None
        for task_instance in self.task_instances:
            if task_instance.started_timestamp is not None:
                if (t is None) or (t > task_instance.started_timestamp):
                    t = task_instance.started_timestamp
        return t

    @property
    def finished_timestamp(self):
        if not self.finished:
            return None
        t = None
        for task_instance in self.task_instances:
            if (t is None) or (t < task_instance.finished_timestamp):
                t = task_instance.finished_timestamp
        return t


class Job(object):
    # task_cls = Task

    def __init__(self, env, job_config):
        self.env = env
        self.job_config = job_config
        self.id = job_config.id
        self.type = job_config.type

        self.tasks_map = {}
        for task_config in job_config.task_configs:
            task_index = task_config.task_index
            self.tasks_map[task_index] = Task(env, self, task_config)

    def reset_job(self):
        self.env = env
        self.job_config = job_config
        self.id = job_config.id
        response_time = self.running_time

        self.tasks_map = {}
        for task_config in job_config.task_configs:
            task_index = task_config.task_index
            task_config.response_time = response_time
            self.tasks_map[task_index] = Task(env, self, task_config)

    @property
    def tasks(self):
        return self.tasks_map.values()

    @property
    def running_time(self):
        max_running_time = 0.0
        ls = unfinished_tasks(self)
        for task in ls:
            if running_time(task) > max_running_time:
                max_running_time = running_time(task)
        return running_time

    @property
    def unfinished_tasks(self):
        ls = []
        for task in self.tasks_map.values():
            if not task.finished:
                ls.append(task)
        return ls

    @property
    def ready_unfinished_tasks(self):
        ls = []
        for task in self.tasks:
            if not task.finished and task.ready:
                ls.append(task)
        return ls

    @property
    def tasks_which_has_waiting_instance(self):
        ls = []
        for task in self.tasks:
            if task.has_waiting_task_instances:
                ls.append(task)
        return ls

    @property
    def ready_tasks_which_has_waiting_instance(self):
        ls = []
        for task in self.tasks:
            if task.has_waiting_task_instances and task.ready:
                ls.append(task)
        return ls

    @property
    def running_tasks(self):
        ls = []
        for task in self.tasks:
            if task.started and not task.finished:
                ls.append(task)
        return ls

    @property
    def finished_tasks(self):
        ls = []
        for task in self.tasks:
            if task.finished:
                ls.append(task)
        return ls

    @property
    def started(self):
        for task in self.tasks:
            if task.started:
                return True
        return False

    @property
    def finished(self):
        for task in self.tasks:
            if not task.finished:
                return False
        return True

    @property
    def started_timestamp(self):
        t = None
        for task in self.tasks:
            if task.started_timestamp is not None:
                if (t is None) or (t > task.started_timestamp):
                    t = task.started_timestamp
        return t

    @property
    def finished_timestamp(self):
        if not self.finished:
            return None
        t = None
        for task in self.tasks:
            if (t is None) or (t < task.finished_timestamp):
                t = task.finished_timestamp
        return t


class TaskInstance(object):
    def __init__(self, env, task, task_instance_index, task_instance_config):
        self.env = env
        self.task = task
        self.task_instance_index = task_instance_index
        self.config = task_instance_config
        self.cpu = task_instance_config.cpu
        self.memory = task_instance_config.memory
        self.disk = task_instance_config.disk
        self.duration = task_instance_config.duration
        self.response_time = task_instance_config.response_time

        self.running_time = 0.0

        self.machine = None
        self.process = None
        self.new = True

        self.waiting = False
        self.running = False
        self.started = False
        self.finished = False
        self.reset = False
        self.started_timestamp = None
        self.finished_timestamp = None

    @property
    def id(self):
        return str(self.task.id) + '-' + str(self.task_instance_index)

    def do_work(self):
        try:
            # assert self.task.task_config.submit_time >= self.env.now
            # timeout_duration = self.task.task_config.submit_time - self.env.now
            # if timeout_duration > 0:
            #     yield self.env.timeout(timeout_duration)
            flag = 0
            # print('Task instance %f of task %f of job %f is executing' %(self.task_instance_index, self.task.task_index, self.task.job.id))
            time_threshold = 300
            div = self.env.now // time_threshold
            if ((self.env.now % time_threshold) == 0 and self.env.now != 0):
                time_threshold = (div) * time_threshold # ama einai akrivws 100,200 klp tote paw sto pause
            else:
                time_threshold = (div+1) * time_threshold # ama einai estw kai 0.1 over tote pausarei sto epomeno checkpoint
            while(not self.finished or self.reset):
                if (((self.env.now + 0.1) / time_threshold) > 1 and self.env.now != 0):
                    flag = 1
                    # print('i am task instance %s of task %s of job %s and i am pausing at time %f' \
                    # 'with threshold %f '% (self.task_instance_index, self.task.task_index, \
                    # self.task.job.id, self.env.now, time_threshold))
                    time_threshold += 301 # perimenei mono thn prwth fora
                    yield self.env.pause_event
                    # yield self.env.timeout(0.001)  # Wait here while the system is paused
                    # print('i am task instance %s of task %s of job %s and i have restarted after pause \
                    #     with metrics %f %f %f' % (self.task_instance_index, self.task.task_index, self.task.job.id, \
                    #     self.cpu, self.memory, self.disk))
                if (self.finished == False and self.waiting == False and self.reset == False):
                    if flag == 1:
                        # print('i am task instance %s of task %s of job %s and i am running at the time moment %f' \
                        # % (self.task_instance_index, self.task.task_index, self.task.job.id, self.env.now))
                        flag = 0
                    self.running_time += 0.1
                    yield self.env.timeout(0.1)
                    if self.running_time >= self.duration:
                        self.finished = True
                elif self.waiting == True:
                    if self.machine.accommodate(self):
                        self.machine.num_waiting_instances -= 1
                        self.waiting = False
                        self.machine.restart_task_instance(self)
                        self.running = True
                    else:
                        # print('i am task instance %s of task %s of job %s and i am waiting for reallocation ' \
                        # 'with running time %f and remaining time %f and flag %s and reset %s' % (self.task_instance_index, \
                        # self.task.task_index, self.task.job.id, self.running_time, self.duration-self.running_time, \
                        # self.machine.accommodate(self), self.reset))
                        while(not self.machine.accommodate(self) and not self.reset):
                            if ((self.env.now + 0.1) / time_threshold > 1 and self.env.now != 0):
                                # print('i am task instance %s of task %s of job %s and i am pausing at time %f' \
                                # % (self.task_instance_index, self.task.task_index, self.task.job.id,self.env.now))
                                time_threshold += 301 # perimenei mono thn prwth fora
                                yield self.env.pause_event
                                # yield self.env.timeout(0.001)  # Wait here while the system is paused
                                # print('i am task instance %s of task %s of job %s and i have restarted after pause, '\
                                #     'with metrics %f %f %f and machine acc flag %s and %s and %s' % (self.task_instance_index, \
                                #     self.task.task_index, self.task.job.id, self.cpu, self.memory, \
                                #     self.disk, self.machine.accommodate(self), self.machine.feature, self.machine.capacity))
                            if (not self.machine.accommodate(self) and not self.reset):
                                yield self.env.timeout(0.5)
                                self.response_time += 0.5
                        self.machine.num_waiting_instances -= 1
                        self.waiting = False
                        self.machine.restart_task_instance(self)
                        if self.reset:
                            # print('i am task instance %s of task %s of job %s and i am reseting' \
                            #     % (self.task_instance_index, self.task.task_index, self.task.job.id))
                            self.reset = False
                            return
                        self.running = True
                        # self.machine.restart_task_instance(self)
                elif self.reset == True:
                    print('i am task instance %s of task %s of job %s and i am reseting' \
                            % (self.task_instance_index, self.task.task_index, self.task.job.id))
                    self.reset = False
                    return

            self.finished_timestamp = self.env.now
            self.running = False
            self.finished = True
            self.machine.stop_task_instance(self)
            # print('Task instance %f of task %f of job %f has finished in %s time with response_time %s' \
            # %(self.task_instance_index, self.task.task_index, self.task.job.id, self.env.now, self.response_time))
    
        except simpy.Interrupt:
            # print('Task instance %f of task %f of job %f has been interrupted and will stop' \
            # %(self.task_instance_index, self.task.task_index, self.task.job.id))
            self.running = False
            self.reset = False
            return
    
    def recalc_metrics(self, new_metrics):
        self.machine.stop_task_instance(self)
        self.cpu = new_metrics[0]
        self.memory = new_metrics[1]
        self.disk = new_metrics[2]
        self.config.cpu = new_metrics[0]
        self.config.memory = new_metrics[1]
        self.config.disk = new_metrics[2]
        if self.machine.accommodate(self):
            self.machine.restart_task_instance(self)
        else:
            self.machine.num_waiting_instances += 1
            self.waiting = True
            self.running = False

    def return_metric(self, num):
        if num == 0:
            return self.cpu
        elif num == 1:
            return self.memory
        elif num == 2:
            return self.disk

    @property
    def avg_metrics(self):
        return (self.cpu + self.memory + self.disk) / 3

    @property
    def metrics(self):
        return [self.cpu, self.memory, self.disk]
    
    @property
    def scheduled_time(self):
        return (self.response_time + self.running_time)

    @property
    def remaining_time(self):
        return (self.duration - self.running_time)

    def refresh_response_time(self, response_time):
        self.response_time = response_time
        self.task.refresh_response_time(self.response_time)

    def passive_refresh_response_time(self, response_time):
        self.response_time = response_time

    def reset_instance(self):
        self.reset = True
        self.response_time = self.response_time + self.running_time
        self.started = False
        self.waiting = False
        self.running = False
        self.machine.stop_task_instance(self)
        self.machine.remove_task_instance(self)
        # config = self.alter_task_config
        # self.task.reset_task_instance(self.task_instance_index, config)

    def schedule(self, machine):
        self.started = True
        self.running = True
        self.started_timestamp = self.env.now
        self.machine = machine
        self.machine.run_task_instance(self)
        self.process = self.env.process(self.do_work())
    
    # def alter_task_config(self):
    #     task_instance_config = TaskInstanceConfig(task.task_config)
    #     task_instance_config.cpu = self.cpu
    #     task_instance_config.memory = self.memory
    #     task_instance_config.disk =  self.disk
    #     task_instance_config.response_time = self.response_time + self.running_time
    #     return task_instance_config
