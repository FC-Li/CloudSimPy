import simpy

from playground.DAG.utils.csv_reader import CSVReader
from core.central_cluster import Cluster
from core.scheduler import Scheduler
from core.broker import Broker
from core.simulation import Simulation
from playground.auxiliary.add_job_config import add_job_config
from playground.auxiliary.print_instances import print_selected_task_instances
from playground.auxiliary.new_task_configs import generate_task_instance_configs
from playground.DAG.algorithm.heuristics.redirect_workloads import redirect_workload



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
        yield self.env.timeout(delay)  # Wait for the specific time interval
        print("Performing actions after pausing...")

        unfinished_task_instances = self.simulation.cluster.unfinished_instances
        print_selected_task_instances(unfinished_task_instances, "unfinished")
        running_task_instances = self.simulation.cluster.running_task_instances
        print_selected_task_instances(running_task_instances, "running")
        waiting_task_instances = self.simulation.cluster.waiting_task_instances
        print_selected_task_instances(waiting_task_instances, "waiting")
        not_started_task_instances = self.simulation.cluster.not_started_task_instances
        print_selected_task_instances(not_started_task_instances, "not_started")

        # Perform required actions here...

        waiting_machines = self.simulation.cluster.machines_only_waiting_instances
        deadlock_waiting_machines = []
        for machine in waiting_machines:
            print(f"waiting machines workloads are {len(machine.waiting_task_instances)}")
            if len(machine.waiting_task_instances) > 1:
                deadlock_waiting_machines.append(machine)
            print(type(machine))
        redirect_workload(deadlock_waiting_machines)
        
        generate_task_instance_configs(self.simulation.cluster.non_waiting_instances)

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
        if (self.simulation.finished != 1 and self.env.now < 5503):
            # yield self.env.timeout(300)
            print('The time at the start of the next pause is', self.env.now + 301.0)
            cnt += 1
            self.env.process(self.trigger_pause_event_after_rl_actions(301, cnt))  # Schedule the pause trigger

