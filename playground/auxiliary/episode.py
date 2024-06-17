import simpy
import os
import pandas as pd
import math, statistics

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
    jobs_csv, method, algorithm, name, learning_rate, layers, loss_func, activ_func, exploration, train_flag, response_time_threshold, event_file):
        self.env = simpy.Environment()
        self.method = method
        self.algorithm = algorithm
        self.response_time_threshold = response_time_threshold
        # Initialize DataFrame
        columns = ['Time', 'Cluster', 'CPU', 'Memory', 'Disk', 'Usage']
        self.df = pd.DataFrame(columns=columns)
        self.kwh_cost = []
        self.train_flag = train_flag

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
            nodes = (machines_number[i] / 3) + ((1 * machines_number[i]) / 3)
            # Round up to the closest integer
            nodes = math.ceil(nodes)
            nodes_cap.append(nodes)
        print(nodes_cap, "the nodes cap is this")
    
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

        near_scheduler = Scheduler(self.env, self.algorithm, 0)
        far_scheduler = Scheduler(self.env, self.algorithm, 1)
        cloud_scheduler = Scheduler(self.env, self.algorithm, 2)

        self.simulation = Simulation(self.env, cluster, task_broker, near_scheduler, far_scheduler, cloud_scheduler, event_file)

        if self.method == 1:
            jobs_num = 92
            # loss_func = loss
            # activ_func = activation
            state_features_num = 10
            actions_features_num = 13
            # layers = 6
            # learning_rate = 0.00001
            # name = "all"
            model_dir = 'DAG/algorithm/DeepJS/agents/%s/%s/%s/%s_%s/%s_%s_%s' % (name, layers, learning_rate,
            loss_func, activ_func, jobs_num, state_features_num, actions_features_num)
            self.model_dir = model_dir
            model_path = os.path.join(model_dir, 'model.pth')  # Change from 'model.h5' to 'model.pth'
            print(model_dir, model_path)
            if os.path.exists(model_path):
                self.agent = DQLAgent(state_features_num, actions_features_num, 0.2, name, jobs_num, layers, learning_rate, loss_func, activ_func, exploration, train_flag)
                self.agent.load_model(model_path)
                print("Loaded a pre-existing model")
            else:
                self.agent = DQLAgent(state_features_num, actions_features_num, 0.2, name, jobs_num, layers, learning_rate, loss_func, activ_func, exploration, train_flag)
            reward_giver = RewardGiver(cluster)
            self.scheduler = DQLScheduler(self.agent, cluster, reward_giver)
            # for i in range(10):
                # cluster.remove_nodes(1, 10)
                # cluster.remove_nodes(0, 10)
            #     cluster.create_nodes(1, 15)
            #     cluster.create_nodes(0, 5)

            self.agent.test_act([[0.5, 0.5, 0.5, 1, 0, 0, 0, 0, 0, 0],
            [0.5, 0.5, 0, 1, 0, 0, 0, 0, 0, 0],
            [0.5, 0, 0.5, 1, 0, 0, 0, 0, 0, 0],
            [0.8, 0.8, 1, 1, 0.02, 0, 0, 0, 0, 0],
            [0.5, 1, 0.5, 1, 0, 0.1, 0, 0, 0, 0],
            [0.5, 1, 0.5, 1, 0, 0, 0.001, 0, 0, 1],
            [0.5, 0, 0.5, 1, 0, 0, 0.001, 0, 0, 1],
            [0.8, 0.8, 1, 1, 0, 0.1, 0.1, 0, 1, 0],
            [0.8, 0.8, 1, 1, 0.02, 0.1, 0.1, 1, 0, 0],
            [0.5, 0.5, 0.5, 1, 0.1, 0.1, 0, 1, 1, 0],
            [0.5, 1, 0.5, 1, 0.1, 0.1, 0, 1, 1, 0],
            [1, 1, 0.5, 1, 0.1, 0.1, 0, 1, 1, 0],
            [0.5, 0.5, 0.5, 1, 0, 0.02, 0, 0, 1, 0],
            [0.5, 0.5, 0, 1, 0, 0.02, 0, 0, 1, 0],
            [0.5, 0.5, 0.5, 1, 0, 0, 0.02, 0, 0, 0],
            [0.5, 0.5, 0, 1, 0, 0, 0.02, 0, 0, 1],
            [1, 0.3, 0.1, 1, 0.1, 0, 0, 1, 0, 0],
            [1, 0.5, 0.5, 1, 0.1, 0, 0, 1, 0, 0],
            [0.5, 0, 1, 0, 0.1, 0.1, 0.1, 1, 1, 1],
            [0, 0.5, 1, 0, 0.1, 0.1, 0.1, 1, 1, 1],
            [0, 0, 0.5, 0, 0.1, 0.1, 0.1, 1, 1, 1],
            [0, 0.5, 0.5, 0, 0.1, 0.1, 0.1, 1, 1, 1],
            [0.5, 0.5, 0.5, 0, 0.1, 0.1, 0.1, 1, 1, 1],
            [0.5, 0.3, 0.5, 1, 0.1, 0.1, 0.1, 1, 1, 1],
            [0.5, 1, 0.5, 1, 0.1, 0.1, 0.1, 1, 1, 1],
            [0.8, 0.3, 0.5, 1, 0.1, 0.1, 0.1, 1, 1, 1],
            [1, 1, 0.5, 1, 0.1, 0.1, 0.1, 1, 1, 1],
            [1, 0.5, 0.5, 1, 0.1, 0.1, 0.1, 1, 1, 1],
            [0.5, 0.5, 0.5, 1, 0.1, 0.1, 0.1, 1, 1, 1],]) 
            # self.agent.test_act([[0.0, 0.0, 0.0, 0.0, 0.003479990740740741, 0.00019905555555555432, 0.9, 0.35714285714285715, 1.0, 0.125, 0.05473672979687258, 0.0, 0.0, 0.0003, 0.0, 0.0, 0.0],
            # [0.0, 0.0, 0.7412052888888888, 0.7318317333333334, 0.0, 0.0, 0.9, 0.35714285714285715, 0.016, 0.125, 0.125, 0.0, 0.0657, 0.0, 0.0, 0.0641, 0.0],
            # [0.0, 0.0, 0.03560407407407407, 0.03550648148148148, 0.9683300000000004, 0.9251822222222224, 0.06666666666666667, 0.8571428571428571, 0.016666666666666666, 0.125, 0.125, 0.0, 0.0076, 0.0082, 0.0, 0.0, 0.0074],
            # [0.2409044444444445, 0.22157, 0.16685066666666665, 0.17248080952380943, 0.23771934567901232, 0.2373433827160493, 0.23333333333333334, 1.0, 0.75, 0.125, 0.125, 0.0063, 0.044, 0.0792, 0.0, 0.0, 0.0],
            # [0.9543233333333334, 0.9564566666666673, 0.9128883547008547, 0.9295299999999995, 0.24331587654320988, 0.23342280246913585, 0.06666666666666667, 0.7428571428571429, 0.75, 0.125, 0.125, 0.0075, 0.1782, 0.0779, 1.3847, 1.0404, 0.0],
            # [0.7844454814814812, 0.7936771111111114, 0.76591426984127, 0.7669897460317456, 0.06570540740740743, 0.062449000000000025, 0.5, 1.0, 1.0, 0.125, 0.125, 0.0428, 0.1955, 0.0273, 0.2017, 0.0, 0.0],
            # [0.9193608888888892, 0.9459131851851854, 0.9402867555555555, 0.908723955555556, 0.8844939247311832, 0.9113925268817208, 0.5, 0.35714285714285715, 0.5166666666666667, 0.125, 0.125, 0.0509, 0.0842, 0.2014, 0.6125, 0.2259, 0.5851],
            # [0.9076800740740744, 0.9334586666666667, 0.9051688253968257, 0.9180810793650797, 0.9083004629629627, 0.9255557222222222, 0.5, 0.5, 0.5, 0.125, 0.03896108464793252, 0.0496, 0.1157, 0.1958, 0.8545, 0.7044, 0.8422]])

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
        not_started_task_instances = self.simulation.cluster.not_started_task_instances
        # print_selected_task_instances(not_started_task_instances, "not_started")

        ls = []
        ls.extend(running_task_instances)
        ls.extend(waiting_task_instances)
        ls.extend(not_started_task_instances)

        # Perform required actions here...

        if self.method == 1:
            # list_states = []
            # self.agent.test_act([[0.0, 0.0, -0.000000000000213, 0.000000000003647367308464056, 0.0026246811594202828, 0.00041104347826087, 0.15, 0.075, 0.39, 0.195, 0.8625, 0.43125, 0.9090909090909091, 0.9454545454545454, 0.8712121212121212, 0.0, 0.1222298099280305, 0.08618184426703664, 0.0, 0.0, 0.0],
            # [0.9656290000000003, 0.4669128333333329, 0.951532266666666, 0.3508053333333343, 0.9606587083333316, 0.32809027777777783, 0.15, 0.075, 0.375, 0.1875, 0.9, 0.45, 0.9090909090909091, 0.9090909090909091, 0.9090909090909091, 0.004645378352490422, 0.004268045371219065, 0.0037719395146685983, 0.04142, 0.04254, 0.05284]])
            if len(ls) > 0:
                current_state = self.scheduler.extract_state(self.response_time_threshold)
                print(current_state)
                self.scheduler.act_on_pause(current_state, 16)

                # generate_task_instance_configs(self.simulation.cluster.non_waiting_instances, self.env.now)

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
        print(overall_averages)
        self.kwh_cost.append(self.simulation.cluster.average_kwh_cost)

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
            if self.env.now > 12000:
                self.simulation.finished == True
            else:
                cnt += 1
                self.env.process(self.trigger_pause_event_after_rl_actions(50, cnt))  # Schedule the pause trigger
        else:
            if self.method == 1 and self.train_flag == 'True':
                self.agent.save_model(self.train_flag)
            print(self.env.now)
            # After collecting all data
            cluster_utils = calculate_overall_averages(self.df, self.simulation.cluster)
            average_type_instances_df(self.simulation.cluster)
            anomaly_2_step_occurancies_df(self.simulation.cluster)
            response_times = instances_response_times_df(self.simulation.cluster)
            separate_response_times = clusters_response_times_df(self.simulation.cluster)
            print("Mean cost of energy consumption:", statistics.mean(self.kwh_cost))
            print("Overall cost of energy consumption:", sum(self.kwh_cost), "$")
            if self.method == 1:
                if self.train_flag == 'False':
                    list = [self.model_dir[28:], self.env.now, statistics.mean(self.kwh_cost), sum(self.kwh_cost), cluster_utils, response_times, separate_response_times]
                    create_and_update_dataframe(list)
            else:
                list = [self.algorithm, self.env.now, statistics.mean(self.kwh_cost), sum(self.kwh_cost), cluster_utils, response_times, separate_response_times]
                create_and_update_dataframe(list)