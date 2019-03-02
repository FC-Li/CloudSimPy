class Scheduler(object):
    def __init__(self, env, algorithm):
        self.env = env
        self.algorithm = algorithm
        self.simulation = None
        self.cluster = None
        self.destroyed = False
        self.valid_pairs = {}

    def attach(self, simulation):
        self.simulation = simulation
        self.cluster = simulation.cluster

    def make_decision(self):
        while True:
            machine, task = self.algorithm(self.cluster, self.env.now)
            if machine is None or task is None:
                break
            else:
                task.start_task_instance(machine)

    def run(self):
        while not self.simulation.finished:
            self.make_decision()
            yield self.env.timeout(1)
        self.destroyed = True
