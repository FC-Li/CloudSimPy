import simpy

from playground.DAG.utils.csv_reader import CSVReader
from core.central_cluster import Cluster
from core.scheduler import Scheduler
from core.broker import Broker
from core.simulation import Simulation
from playground.auxiliary.add_job_config import add_job_config
from playground.auxiliary.new_task_configs import generate_task_instance_configs



class Episode(object):
    broker_cls = Broker

    def __init__(self, machine_groups, node_configs, jobs_csv, algorithm, event_file):
        self.env = simpy.Environment()

        csv_reader = CSVReader(jobs_csv, self.env.now)
        jobs_configs = csv_reader.generate(0, 9)
        
        self.env.pause_event = simpy.Event(self.env)  # Corrected to use self.env
        event_cnt = 1
        self.env.process(self.trigger_pause_event_after_rl_actions(301, event_cnt))  # Schedule the pause trigger
        
        # Your setup continues here...
        # cluster, task_broker, scheduler initialization...
        cluster = Cluster()
        cluster.child_clusters = [Cluster(level=i) for i in range(3)]  # Create 3 child clusters
        for node_config in node_configs:
            if node_config.id in machine_groups:  # Check if there are machines for this node_id
                node_config.add_machines(machine_groups[node_config.id])
        cluster.add_nodes(node_configs)

        task_broker = Episode.broker_cls(self.env, jobs_configs)

        near_scheduler = Scheduler(self.env, algorithm, 0)
        far_scheduler = Scheduler(self.env, algorithm, 1)
        cloud_scheduler = Scheduler(self.env, algorithm, 2)

        self.simulation = Simulation(self.env, cluster, task_broker, near_scheduler, far_scheduler, cloud_scheduler, event_file)

    def run(self):
        self.simulation.run()
        self.env.run()

    def trigger_pause_event_after_rl_actions(self, delay, cnt):
        tasks_list = []
        yield self.env.timeout(delay)  # Wait for the specific time interval
        print("Performing actions after pausing...")
        unfinished_task_instances = self.simulation.cluster.unfinished_instances
        for task_instance in unfinished_task_instances:
            tasks_list.append((task_instance.task.job.id, \
            task_instance.task.task_index, task_instance.task_instance_index, task_instance.machine.id))
        print(f"Unfinished tasks: {tasks_list}")
        # Perform required actions here...
        
        generate_task_instance_configs(unfinished_task_instances)

        # jobs_configs2 = add_job_config(self.simulation, Episode.broker_cls, cnt)
        
        '''
        Here i will call funcs to perform the rl model actions based on the system state!!
        '''
        print("Finished with the actions")
        # yield self.env.timeout(300)
        self.env.pause_event.succeed()  # Trigger the pause
        print("Pause event triggered")
        # Reset the pause event for future use if needed
        self.env.pause_event = simpy.Event(self.env)
        if (self.simulation.finished != 1 and self.env.now < 1503):
            # yield self.env.timeout(300)
            print('The time at the start of the next pause is', self.env.now + 301.0)
            cnt += 1
            self.env.process(self.trigger_pause_event_after_rl_actions(301, cnt))  # Schedule the pause trigger

