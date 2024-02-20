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
    def finished_task_instances(self):
        ls = []
        for task_instance in self.task_instances:
            if task_instance.finished:
                ls.append(task_instance)
        return ls

    # the most heavy
    def start_task_instance(self, machine):
        self.task_instances[self.next_instance_pointer].schedule(machine)
        self.next_instance_pointer += 1

    def reset_task_instance(self):
        task_instance_config = TaskInstanceConfig(task_config)
        task_instance_config.response_time = self.env.now
        self.task_config.instances_number = str(int(self.task_config.instances_number) + 1)
        self.task_instances.append(TaskInstance(self.env, self, task_instance_index, task_instance_config))

    def refresh_response_time(self, response_time):
        self.response_time = response_time
        for i in range(int(self.next_instance_pointer+1), int(self.task_config.instances_number)):
            self.task_instances[i].passive_refresh_response_time(response_time)

    @property
    def started(self):
        for task_instance in self.task_instances:
            if task_instance.started:
                return True
        return False

    @property
    def waiting_task_instances_number(self):
        return self.task_config.instances_number - self.next_instance_pointer

    @property
    def has_waiting_task_instances(self):
        return self.task_config.instances_number > self.next_instance_pointer

    @property
    def finished(self):
        """
        A task is finished only if it has no waiting task instances and no running task instances.
        :return: bool
        """
        if self.has_waiting_task_instances:
            return False
        if len(self.running_task_instances) != 0:
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
    task_cls = Task

    def __init__(self, env, job_config):
        self.env = env
        self.job_config = job_config
        self.id = job_config.id
        self.response_time = job_config.response_time

        self.tasks_map = {}
        for task_config in job_config.task_configs:
            task_index = task_config.task_index
            self.tasks_map[task_index] = Job.task_cls(env, self, task_config)

    @property
    def tasks(self):
        return self.tasks_map.values()

    @property
    def unfinished_tasks(self):
        ls = []
        for task in self.tasks:
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

        self.machine = None
        self.process = None
        self.new = True

        self.started = False
        self.finished = False
        self.started_timestamp = None
        self.finished_timestamp = None

    @property
    def id(self):
        return str(self.task.id) + '-' + str(self.task_instance_index)

    def do_work(self):
        # self.cluster.waiting_tasks.remove(self)
        # self.cluster.running_tasks.append(self)
        # self.machine.run(self)
        print('Task instance %f of task %f of job %f is executing' %(self.task_instance_index, self.task.task_index, self.task.job.id))
        steps = int(self.duration / 0.001)  # Convert execution time to number of steps
        time_threshold = 100
        div = self.env.now / time_threshold
        if ((self.env.now % time_threshold) == 0 and self.env.now != 0):
            time_threshold = (div) * time_threshold # ama einai akrivws 100,200 klp tote paw sto pause
        else:
            time_threshold = (div+1) * time_threshold # ama einai estw kai 0.1 over tote pausarei sto epomeno checkpoint
        for step in range(steps):
            if (self.env.now / time_threshold >= 1 and self.env.now != 0):
                time_threshold += 100 # perimenei mono thn prwth fora
                yield self.env.pause_event
                # yield self.env.timeout(0.001)  # Wait here while the system is paused
            # yield self.env.timeout(self.duration)
            yield self.env.timeout(0.001)  # Wait here while the system is paused


        self.finished = True
        self.finished_timestamp = self.env.now
        print('Task instance %f of task %f of job %f has finished in %s time with response_time %s' \
        %(self.task_instance_index, self.task.task_index, self.task.job.id, self.env.now, self.response_time))

        self.machine.stop_task_instance(self)

    def refresh_response_time(self, response_time):
        self.response_time = response_time
        self.task.refresh_response_time(self.response_time)

    def passive_refresh_response_time(self, response_time):
        self.response_time = response_time

    def schedule(self, machine):
        self.started = True
        self.started_timestamp = self.env.now
        self.machine = machine
        self.machine.run_task_instance(self)
        self.process = self.env.process(self.do_work())
