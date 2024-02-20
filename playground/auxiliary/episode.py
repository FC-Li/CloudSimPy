import simpy

from playground.DAG.utils.csv_reader import CSVReader
from core.central_cluster import Cluster
from core.scheduler import Scheduler
from core.broker import Broker
from core.simulation import Simulation
from playground.auxiliary.add_job_config import add_job_config



class Episode(object):
    broker_cls = Broker

    def __init__(self, machine_configs, jobs_csv, algorithm, event_file):
        self.env = simpy.Environment()

        csv_reader = CSVReader(jobs_csv, self.env.now)
        jobs_configs = csv_reader.generate(0, 9)
        
        self.env.pause_event = simpy.Event(self.env)  # Corrected to use self.env
        self.env.process(self.trigger_pause_event_after_rl_actions(301))  # Schedule the pause trigger
        
        # Your setup continues here...
        # cluster, task_broker, scheduler initialization...
        cluster = Cluster()
        cluster.child_clusters = [Cluster(level=i) for i in range(3)]  # Create 3 child clusters
        cluster.add_machines(machine_configs)
        # cluster = Cluster()
        # cluster.add_machines(machine_configs)

        task_broker = Episode.broker_cls(self.env, jobs_configs)

        near_scheduler = Scheduler(self.env, algorithm, 0)
        far_scheduler = Scheduler(self.env, algorithm, 1)
        cloud_scheduler = Scheduler(self.env, algorithm, 2)

        self.simulation = Simulation(self.env, cluster, task_broker, near_scheduler, far_scheduler, cloud_scheduler, event_file)

    def run(self):
        self.simulation.run()
        self.env.run()

    def trigger_pause_event_after_rl_actions(self, delay):
        tasks_list = []
        yield self.env.timeout(delay)  # Wait for the specific time interval
        print("Performing actions after pausing...")
        unfinished_tasks = self.simulation.cluster.unfinished_tasks
        for task in unfinished_tasks:
            tasks_list.append(task.task_index)
        print(f"Unfinished tasks: {tasks_list}")
        # Perform required actions here...
        jobs_configs2 = add_job_config(self.simulation, Episode.broker_cls)
        
        '''
        Here i will call funcs to perform the rl model actions based on the system state!!
        '''
        print("Finished with the actions")
        yield self.env.timeout(100)
        self.env.pause_event.succeed()  # Trigger the pause
        print("Pause event triggered")
        # Reset the pause event for future use if needed
        self.env.pause_event = simpy.Event(self.env)
        while not self.simulation.finished:
            print('The time at the start of the next pause is', self.env.now)
            yield self.env.timeout(300)
            self.env.process(self.trigger_pause_event_after_rl_actions(1))  # Schedule the pause trigger

