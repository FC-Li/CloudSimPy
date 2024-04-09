import simpy
import os
import pandas as pd
import math

from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
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
from playground.auxiliary.update_df_with_averages import *
from playground.DAG.algorithm.heuristics.redirect_workloads import redirect_workload


class Episode(object):
    broker_cls = Broker

    def __init__(self, machine_groups, machines_number, node_configs, \
    jobs_csv, algorithm, event_file):
        self.env = simpy.Environment()
        self.method = 1

        csv_reader = CSVReader(jobs_csv, self.env.now)
        jobs_num = csv_reader.get_total_jobs()
        jobs_configs = csv_reader.generate(0, jobs_num)
        
        self.env.pause_event = simpy.Event(self.env)  # Corrected to use self.env
        event_cnt = 1
        self.env.process(self.trigger_pause_event_after_rl_actions(50, event_cnt))  # Schedule the pause trigger
        
        # Your setup continues here...
        # cluster, task_broker, scheduler initialization...
        nodes_cap = []
        for i in range(3):
            nodes = (machines_number[i] / 3) + ((0.1 * machines_number[i]) / 3)
            # Round up to the closest integer
            nodes = math.ceil(nodes)
            nodes_cap.append(nodes)
    
        cluster = Cluster()
        cluster.child_clusters.append(Cluster(0, nodes_cap[0]))
        cluster.child_clusters.append(Cluster(1, nodes_cap[1]))
        cluster.child_clusters.append(Cluster(2, nodes_cap[2]))
        # cluster.child_clusters.append(Cluster(0, (machines_number[0] * 2) / 3))
        # cluster.child_clusters.append(Cluster(1, (machines_number[1] * 2) / 3))
        # cluster.child_clusters.append(Cluster(2, (machines_number[2] * 2) / 3))

        # Iterate over node_configs to add machines based on the modified key structure
        for node_config in node_configs:
            key = (node_config.topology, node_config.id)
            # Check if the constructed key matches any entry in machine_groups
            if key in machine_groups:
                # Use the machines associated with the constructed key
                node_config.add_machines(machine_groups[key])
        cluster.add_nodes(node_configs)

        task_broker = Episode.broker_cls(self.env, jobs_configs)

        near_scheduler = Scheduler(self.env, algorithm, 0)
        far_scheduler = Scheduler(self.env, algorithm, 1)
        cloud_scheduler = Scheduler(self.env, algorithm, 2)

        self.simulation = Simulation(self.env, cluster, task_broker, near_scheduler, far_scheduler, cloud_scheduler, event_file)

        if self.method == 1:
            jobs_num = 86
            state_features_num = 18
            actions_features_num = 13
            model_dir = 'DAG/algorithm/DeepJS/agents/all/%s_%s_%s' % (jobs_num, state_features_num, actions_features_num)
            model_path = os.path.join(model_dir, 'model.h5')
            print(model_dir, model_path)
            if os.path.exists(model_path):
                model = load_model(model_path, custom_objects={'loss': MeanSquaredError()})
                model.compile(optimizer='adam', loss='mean_squared_error')
                # model.compile(optimizer='adam', loss='mse')
                self.agent = DQLAgent(state_features_num, actions_features_num, 0.7, jobs_num, model)
                print("i loaded a pre-existing model")
            else:
                self.agent = DQLAgent(state_features_num, actions_features_num, 0.7, jobs_num)
            reward_giver = RewardGiver(cluster)
            self.scheduler = DQLScheduler(self.agent, cluster, reward_giver)
                    # list_states = []
            self.agent.test_act([[0.0, 0.0, 0.0, 0.0, 0.007131666666666727, 0.043386666666666664, 0.7727272727272727, 0.922077922077922, 0.0106951871657754, 0.08452890547263668, 0.07726704263463588, 0.05793476791682136, 0.0, 0.0, 0.0001, 0.0, 0.0, 0.0],
            [0.540971574074074, 0.9572164814814814, 0.04936627450980392, 0.1182057843137255, 0.0, 0.0, 0.8181818181818182, 0.8831168831168831, 0.0106951871657754, 0.12569771161793955, 0.048322363087871315, 0.030881088591725836, 0.0428, 0.019, 0.0, 0.145, 0.0003, 0.0],
            [0.0, 0.0, 0.0009304901960784346, 0.0008651470588235276, 0.4596383333333334, 0.8169683333333332, 0.7272727272727273, 0.8831168831168831, 0.0106951871657754, 0.08452890547263668, 0.07726704263463588, 0.05753374303750461, 0.0, 0.0002, 0.0043, 0.0, 0.0, 0.0222],
            [0.5421912500000001, 0.9621165000000002, 0.022496128205128182, 0.027761897435897426, 0.1687041025641025, 0.42505538461538467, 0.9090909090909091, 0.8441558441558441, 0.06951871657754011, 0.10320387985670984, 0.027532133114640926, 0.029965309906502743, 0.0552, 0.0041, 0.0114, 0.3587, 0.0, 0.0002],
            [0.5222885185185185, 0.9558048148148147, 0.15510303921568627, 0.3489559803921568, 0.0, 0.0, 0.8181818181818182, 0.8831168831168831, 0.0106951871657754, 0.116377958801498, 0.06467299101502177, 0.030881088591725836, 0.0414, 0.0535, 0.0, 0.0877, 0.0007, 0.0],
            [0.5665562698412699, 0.9118379365079363, 0.1715819761904761, 0.31373485714285715, 0.03622216802168021, 0.08421016260162602, 0.9545454545454546, 0.9090909090909091, 0.6577540106951871, 0.0342800184774575, 0.017328618887644635, 0.0011903963414634149, 0.0514, 0.051, 0.023, 0.1135, 0.0006, 0.0012],
            [0.5561595, 0.9348481666666667, 0.403806738095238, 0.8147615238095235, 0.1632830674846626, 0.2907995501022495, 0.9090909090909091, 0.9090909090909091, 0.8716577540106952, 0.015965896253602303, 0.003932856396866831, 0.00044042344173441376, 0.0505, 0.1499, 0.1243, 0.2515, 0.0075, 0.0041],
            [0.4398364166666667, 0.9590621666666663, 0.4895883571428572, 0.9443160952380956, 0.2720516458333334, 0.5268413333333334, 0.9090909090909091, 0.9090909090909091, 0.8556149732620321, 0.007934239564428312, 0.0033939277566539926, 0.0002587974254742554, 0.0457, 0.1645, 0.2095, 0.2094, 0.0733, 0.0045]])
        
        # Initialize DataFrame
        columns = ['Time', 'Cluster', 'CPU', 'Memory', 'Disk']
        self.df = pd.DataFrame(columns=columns)

    def run(self):
        self.simulation.run()
        self.env.run()

    def trigger_pause_event_after_rl_actions(self, delay, cnt):
        yield self.env.timeout(delay)  # Wait for the specific time interval
        print("Performing actions after pausing at time ", self.env.now)

        # if self.env.now > 5000:
        #     unfinished_task_instances = self.simulation.cluster.unfinished_task_instances
        #     print_selected_task_instances(unfinished_task_instances, "unfinished")
        #     print(self.env.now)
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

        if self.method == 1:
            # list_states = []
            # self.agent.test_act([[0.0, 0.0, -0.000000000000213, 0.000000000003647367308464056, 0.0026246811594202828, 0.00041104347826087, 0.15, 0.075, 0.39, 0.195, 0.8625, 0.43125, 0.9090909090909091, 0.9454545454545454, 0.8712121212121212, 0.0, 0.1222298099280305, 0.08618184426703664, 0.0, 0.0, 0.0],
            # [0.9656290000000003, 0.4669128333333329, 0.951532266666666, 0.3508053333333343, 0.9606587083333316, 0.32809027777777783, 0.15, 0.075, 0.375, 0.1875, 0.9, 0.45, 0.9090909090909091, 0.9090909090909091, 0.9090909090909091, 0.004645378352490422, 0.004268045371219065, 0.0037719395146685983, 0.04142, 0.04254, 0.05284]])
            if len(ls) > 0:
                current_state = self.scheduler.extract_state()
                print(current_state)
                self.scheduler.act_on_pause(current_state, 16)

                generate_task_instance_configs(self.simulation.cluster.non_waiting_instances)

                for machine in self.simulation.cluster.cluster_machines:
                    machine.check_machine_usage()
                print('the total number of machines is %f and there are %f in edge,'\
                '%f in far edge and %f in the Cloud' %(len(self.simulation.cluster.cluster_machines),\
                len(self.simulation.cluster.child_clusters[0].cluster_machines),\
                len(self.simulation.cluster.child_clusters[1].cluster_machines),\
                len(self.simulation.cluster.child_clusters[2].cluster_machines)))
            
        # for child in self.simulation.cluster.child_clusters:
        #     if len(child.running_task_instances) < 5 and self.env.now > 5000:
        #         for instance in child.unfinished_instances:
        #             print('i am task instance %s of task %s of job %s with running flag %s,' \
        #             'waiting flag %s,started flag %s, reset %s, finished %s, machine %s and cluster %s ' \
        #             'and running time %f and remaining time %f' % (instance.task_instance_index, \
        #             instance.task.task_index, instance.task.job.id, instance.running, instance.waiting, \
        #             instance.started, instance.reset, instance.finished, instance.machine, child.level, \
        #             instance.running_time, instance.duration - instance.running_time))
        self.df = update_df_with_averages(self.df, self.simulation.cluster, self.env.now)
        overall_averages = calculate_overall_averages(self.df, self.simulation.cluster)
        # print(overall_averages)

        if self.method == 0:
            waiting_machines = self.simulation.cluster.machines_only_waiting_instances
            deadlock_waiting_machines = []
            for machine in waiting_machines:
                # print(f"waiting machines workloads are {len(machine.waiting_task_instances)}")
                if len(machine.waiting_task_instances) > 1:
                    deadlock_waiting_machines.append(machine)
            redirect_workload(deadlock_waiting_machines)

        # jobs_configs2 = add_job_config(self.simulation, Episode.broker_cls, cnt)
        
        '''
        Here i will call funcs to perform the rl model actions based on the system state!!
        '''
        print("Finished with the actions at time" , self.env.now)
        # yield self.env.timeout(300)
        self.env.pause_event.succeed()  # Trigger the pause
        # print("Pause event triggered")
        # Reset the pause event for future use if needed
        self.env.pause_event = simpy.Event(self.env)
        if (not self.simulation.finished):
            # yield self.env.timeout(300)
            # print('The time at the start of the next pause is', self.env.now + 301.0)
            cnt += 1
            self.env.process(self.trigger_pause_event_after_rl_actions(50, cnt))  # Schedule the pause trigger
        else:
            if self.method == 1:
                self.agent.save_model()
            print(self.env.now)
            # After collecting all data
            overall_averages = calculate_overall_averages(self.df, self.simulation.cluster)
            print(overall_averages)
            average_type_instances_df(self.simulation.cluster)
            anomaly_2_step_occurancies_df(self.simulation.cluster)
            type_instances_response_times_df(self.simulation.cluster)

