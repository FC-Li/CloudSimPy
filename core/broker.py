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
        print("broker_runs")
        for job_config in self.job_configs:
            print(job_config.submit_time,self.env.now, job_config.id)
            assert job_config.submit_time >= self.env.now
            timeout_duration = job_config.submit_time - self.env.now
            if timeout_duration > 0:
                yield self.env.timeout(timeout_duration)
            # yield self.env.timeout(0)
            job = Broker.job_cls(self.env, job_config)
            print('a job arrived at time %f' % self.env.now)
            self.cluster.add_job(job)
        self.destroyed = True
