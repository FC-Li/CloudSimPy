from operator import attrgetter
import pandas as pd
import numpy as np

from core.job import JobConfig, TaskConfig
from playground.DAG.utils.feature_synthesize import father_task_indices


class CSVReader(object):
    def __init__(self, filename, clock):
        self.filename = filename
        df = pd.read_csv(self.filename)

        df.job_id = df.job_id.astype(dtype=int)
        df.instances_num = df.instances_num.astype(dtype=int)

        job_task_map = {}
        job_submit_time_map = {}
        job_response_time_map = {}
        job_type = {}

        # Calculate the total number of unique jobs
        self.total_jobs = df.job_id.nunique()

        cnt_all_instances = 0

        for i in range(len(df)):
            series = df.iloc[i]
            job_id = series.job_id
            task_id, parent_indices = father_task_indices(series.task_id)
            cpu = series.cpu
            memory = series.memory
            disk = series.disk
            duration = series.duration
            submit_time = series.submit_time + clock
            response_time = series.response_time
            instances_num = series.instances_num
            type = series.type

            task_configs = job_task_map.setdefault(job_id, [])
            task_configs.append(TaskConfig(task_id, instances_num, cpu, memory, disk, duration, \
            response_time , submit_time, cnt_all_instances, parent_indices))
            task_configs.sort(key=attrgetter('submit_time'))
            job_submit_time_map[job_id] = submit_time
            job_response_time_map[job_id] = response_time
            job_type[job_id] = type   

            cnt_all_instances += instances_num

        job_configs = []
        for job_id, task_configs in job_task_map.items():
            job_configs.append(JobConfig(job_id, job_submit_time_map[job_id], job_response_time_map[job_id], \
            job_type[job_id], task_configs))
        job_configs.sort(key=attrgetter('submit_time'))
        self.job_configs = job_configs
        # for job in job_configs:
        #     print(job.submit_time)
        # print("the total number of instances is ", cnt_all_instances)

    # Method to access the total number of jobs
    def get_total_jobs(self):
        return self.total_jobs

    def generate(self, offset, number):
        number = number if offset + number < len(self.job_configs) else len(self.job_configs) - offset
        ret = self.job_configs[offset: offset + number]
        the_first_job_config = ret[0]
        submit_time_base = 0

        tasks_number = 0
        task_instances_numbers = []
        task_instances_durations = []
        task_instances_cpu = []
        task_instances_memory = []
        for job_config in ret:
            job_config.submit_time -= submit_time_base
            tasks_number += len(job_config.task_configs)
            for task_config in job_config.task_configs:
                task_config.submit_time -= submit_time_base
                task_instances_numbers.append(task_config.instances_number)
                task_instances_durations.extend([task_config.duration] * int(task_config.instances_number))
                task_instances_cpu.extend([task_config.cpu] * int(task_config.instances_number))
                task_instances_memory.extend([task_config.memory] * int(task_config.instances_number))

        # print('Jobs number: ', len(ret))
        # print('Tasks number:', tasks_number)

        # print('Task instances number mean: ', np.mean(task_instances_numbers))
        # print('Task instances number std', np.std(task_instances_numbers))

        # print('Task instances cpu mean: ', np.mean(task_instances_cpu))
        # print('Task instances cpu std: ', np.std(task_instances_cpu))

        # print('Task instances memory mean: ', np.mean(task_instances_memory))
        # print('Task instances memory std: ', np.std(task_instances_memory))

        # print('Task instances duration mean: ', np.mean(task_instances_durations))
        # print('Task instances duration std: ', np.std(task_instances_durations))

        return ret
