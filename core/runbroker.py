class RunBroker(object):
    def __init__(self, env, simulation, task_broker):
        self.env = env
        self.task_broker = task_broker
        self.simulation = simulation

        self.task_broker.attach(self.simulation)

    def run(self):
        ("runbroker works")
        self.env.process(self.task_broker.run())