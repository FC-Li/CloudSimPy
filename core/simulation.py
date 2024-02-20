from core.monitor import Monitor


class Simulation(object):
    def __init__(self, env, cluster, task_broker, near_scheduler, far_scheduler, cloud_scheduler, event_file):
        self.env = env
        self.cluster = cluster
        self.task_broker = task_broker
        self.near_scheduler = near_scheduler
        self.far_scheduler = far_scheduler
        self.cloud_scheduler = cloud_scheduler
        self.event_file = event_file
        if event_file is not None:
            self.monitor = Monitor(self)

        self.task_broker.attach(self)
        self.near_scheduler.attach(self)
        self.far_scheduler.attach(self)
        self.cloud_scheduler.attach(self)

    def run(self):
        # Starting monitor process before task_broker process
        # and scheduler process is necessary for log records integrity.
        if self.event_file is not None:
            self.env.process(self.monitor.run())
        self.env.process(self.task_broker.run())

        print("i got in the loop with the mutliple scheduler instances and im the cluster", self.cluster.child_clusters[0].level)
        self.env.process(self.near_scheduler.run(self.cluster.child_clusters[0]))
        print("i got in the loop with the mutliple scheduler instances and im the cluster", self.cluster.child_clusters[1].level)
        self.env.process(self.far_scheduler.run(self.cluster.child_clusters[1]))
        print("i got in the loop with the mutliple scheduler instances and im the cluster", self.cluster.child_clusters[2].level)
        self.env.process(self.cloud_scheduler.run(self.cluster.child_clusters[2]))

    @property
    def finished(self):
        return self.task_broker.destroyed \
               and len(self.cluster.unfinished_jobs) == 0
