import random

from core.job import Job

class Broker(object):
    job_cls = Job

    def __init__(self, env, job_configs):
        self.env = env
        self.simulation = None
        self.cluster = None
        self.destroyed = False
        self.job_configs = job_configs

    def attach(self, simulation):
        self.simulation = simulation
        self.cluster = simulation.cluster

    def run(self):
        starting_time = self.env.now
        print("broker_runs with starting time", starting_time)
        for job_config in self.job_configs:
            print(job_config.submit_time,self.env.now, job_config.id)
            assert job_config.submit_time >= self.env.now
            timeout_duration = job_config.submit_time - self.env.now
            if timeout_duration > 0:
                yield self.env.timeout(timeout_duration)
            # yield self.env.timeout(0)
            job = Broker.job_cls(self.env, job_config)
            print('job %s arrived at time %f with the broker that started at %s' % (job.id, self.env.now, starting_time))
            random.choice(self.cluster.child_clusters).add_job(job)
        self.destroyed = True
