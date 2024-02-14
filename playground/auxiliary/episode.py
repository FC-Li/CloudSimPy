import simpy
from core.cluster import Cluster
from core.scheduler import Scheduler
from core.broker import Broker
from core.simulation import Simulation


class Episode(object):
    broker_cls = Broker

    def __init__(self, machine_configs, jobs_configs, algorithm, event_file):
        self.env = simpy.Environment()
        
        self.env.pause_event = simpy.Event(self.env)  # Corrected to use self.env
        self.env.process(self.trigger_pause_event_after_rl_actions(301))  # Schedule the pause trigger
        
        # Your setup continues here...
        # cluster, task_broker, scheduler initialization...
        cluster = Cluster()
        cluster.add_machines(machine_configs)

        task_broker = Episode.broker_cls(self.env, jobs_configs)

        scheduler = Scheduler(self.env, algorithm)

        self.simulation = Simulation(self.env, cluster, task_broker, scheduler, event_file)

    def run(self):
        self.simulation.run()
        self.env.run()

    def trigger_pause_event_after_rl_actions(self,delay):
        tasks_list = []
        print("Performing actions before pausing...")
        yield self.env.timeout(delay)  # Wait for the specific time interval
        unfinished_tasks = self.simulation.cluster.unfinished_tasks
        for task in unfinished_tasks:
            tasks_list.append(task.task_index)
        print(f"Unfinished tasks: {tasks_list}")
        # Perform required actions here...
        '''
        Here i will call funcs to perform the rl model actions based on the system state!!
        '''
        print("Finished with the actions")
        yield self.env.timeout(100)
        self.env.pause_event.succeed()  # Trigger the pause
        print("Pause event triggered")
        # Reset the pause event for future use if needed
        self.pause_event = simpy.Event(self.env)
