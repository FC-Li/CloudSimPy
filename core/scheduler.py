class Scheduler(object):
    def __init__(self, env, algorithm, level=None):
        self.env = env
        self.algorithm = algorithm
        self.simulation = None
        self.cluster = None
        self.destroyed = False
        self.valid_pairs = {}
        self.level = level  
        
    def attach(self, simulation):
        self.simulation = simulation
    #     self.cluster = cluster

    def make_decision(self):
        matched_items, unmatched_tasks = self.algorithm(self.cluster, self.env.now)
        # yield self.env.timeout(100)
        yield self.env.pause_event
        # print("come on")
        for unmatched_task in unmatched_tasks:
            print(unmatched_task.task_index)

        #SOS edw exw ta unmatched tasks na ta dwsw sto rl 
        # print(unmatched_tasks)

    def run(self, cluster):
        # self.attach(self.simulation, cluster)
        self.cluster = cluster
        while not self.simulation.finished:
            print("im the scheduler of the cluster", self.cluster.level)
            yield from self.make_decision()
            # yield self.env.timeout(300) # kanw mia fora to make decision gia kathe time frame anamesa stis apofaseis tou rl
            # print("another passing from the make decision in scheduler")
        self.destroyed = True
