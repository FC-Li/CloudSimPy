import simpy
import os

from playground.DAG.utils.csv_reader import CSVReader
from core.central_cluster import Cluster
from core.scheduler import Scheduler
from core.broker import Broker
from core.simulation import Simulation
from playground.DAG.algorithm.DeepJS.DQLAgent import DQLAgent
from playground.DAG.algorithm.DeepJS.DQLScheduler import DQLScheduler
from playground.DAG.algorithm.DeepJS.reward_giver2 import RewardGiver
from playground.auxiliary.add_job_config import add_job_config
from playground.auxiliary.print_instances import print_selected_task_instances
from playground.auxiliary.new_task_configs import generate_task_instance_configs
from playground.DAG.algorithm.heuristics.redirect_workloads import redirect_workload



class Episode(object):
    broker_cls = Broker

    def __init__(self, machine_groups, node_configs, jobs_csv, jobs_num, algorithm, event_file):
        self.env = simpy.Environment()

        csv_reader = CSVReader(jobs_csv, self.env.now)
        jobs_configs = csv_reader.generate(0, jobs_num)
        
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

        model_dir = 'DAG/algorithm/DeepJS/agents/%s' % jobs_num
        if os.path.isdir(model_dir):
            model = load_model(model_dir)
            self.agent = DQLAgent(39, 12, 0.001, jobs_num, model)
        else:
            self.agent = DQLAgent(39, 12, 0.001, jobs_num)
        reward_giver = RewardGiver(cluster)
        self.scheduler = DQLScheduler(self.agent, cluster, reward_giver)

    def run(self):
        self.simulation.run()
        self.env.run()

    def trigger_pause_event_after_rl_actions(self, delay, cnt):
        yield self.env.timeout(delay)  # Wait for the specific time interval
        # print("Performing actions after pausing...")

        if self.env.now > 5000:
            unfinished_task_instances = self.simulation.cluster.unfinished_task_instances
            print_selected_task_instances(unfinished_task_instances, "unfinished")
            print(self.env.now)
        running_task_instances = self.simulation.cluster.running_task_instances
        # print_selected_task_instances(running_task_instances, "running")
        waiting_task_instances = self.simulation.cluster.waiting_task_instances
        # print_selected_task_instances(waiting_task_instances, "waiting")
        # not_started_task_instances = self.simulation.cluster.not_started_task_instances
        # print_selected_task_instances(not_started_task_instances, "not_started")

        ls = []
        ls.extend(running_task_instances)
        ls.extend(waiting_task_instances)

        # Perform required actions here...
        if len(ls) > 0:
            current_state = self.scheduler.extract_state()
            print(current_state)
            self.scheduler.act_on_pause(current_state, 4)

            generate_task_instance_configs(self.simulation.cluster.non_waiting_instances)

            for machine in self.simulation.cluster.cluster_machines:
                machine.check_machine_usage()

        # waiting_machines = self.simulation.cluster.machines_only_waiting_instances
        # deadlock_waiting_machines = []
        # for machine in waiting_machines:
        #     # print(f"waiting machines workloads are {len(machine.waiting_task_instances)}")
        #     if len(machine.waiting_task_instances) > 1:
        #         deadlock_waiting_machines.append(machine)
        # redirect_workload(deadlock_waiting_machines)

        # jobs_configs2 = add_job_config(self.simulation, Episode.broker_cls, cnt)
        
        '''
        Here i will call funcs to perform the rl model actions based on the system state!!
        '''
        # print("Finished with the actions")
        # yield self.env.timeout(300)
        self.env.pause_event.succeed()  # Trigger the pause
        # print("Pause event triggered")
        # Reset the pause event for future use if needed
        self.env.pause_event = simpy.Event(self.env)
        if (not self.simulation.finished):
            # yield self.env.timeout(300)
            # print('The time at the start of the next pause is', self.env.now + 301.0)
            cnt += 1
            self.env.process(self.trigger_pause_event_after_rl_actions(301, cnt))  # Schedule the pause trigger
        else:
            self.agent.save_model()
            print(self.env.now)

