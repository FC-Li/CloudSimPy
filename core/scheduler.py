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
        matched_items, unmatched_tasks = self.algorithm(self.cluster, self.env.now)
        #SOS edw exw ta unmatched tasks na ta dwsw sto rl 
        # print(unmatched_tasks)


    def run(self):
        flag = True
        while not self.simulation.finished:
            self.make_decision()
            #SOSSSSSS edw mporw na valw timeout analogo me to posos xronos tha apaiteitai gia 
            #na kanei tis energeies to rl model
            yield self.env.pause_event
            print("another passing from the make decision in scheduler")
        self.destroyed = True
