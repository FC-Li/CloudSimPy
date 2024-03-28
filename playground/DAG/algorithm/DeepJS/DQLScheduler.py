import numpy as np

from playground.DAG.algorithm.heuristics.redirect_workloads import *

class DQLScheduler:
    def __init__(self, agent, cluster, reward_giver):
        self.agent = agent
        self.reward_giver = reward_giver
        self.cluster = cluster
        self.last_state = None
        self.last_action = None

    def act_on_pause(self, current_state, batch_size):

        # Calculate reward and next state only if update_model is True and there's a last_state
        reward = self.reward_giver.get_overall_reward()  # Implement reward calculation

        current_state = np.array(current_state, dtype=np.float32)
        current_state = np.expand_dims(current_state, axis=0)  # Add batch dimension
        if self.last_state is not None:
            self.agent.remember(self.last_state, self.last_action, reward, current_state, False)
        
            if len(self.agent.memory) > batch_size:
                self.agent.replay(batch_size)

        # Select and apply action for the current pause
        self.last_action = self.agent.act(current_state)
        self.apply_action(self.last_action)
        self.last_state = current_state  # Store current state for the next call

    def extract_state(self):
        state = []
        usage = self.cluster.usage
        capacities = self.cluster.capacities
        state.extend(usage)
        state.extend(capacities)
        active_nodes = self.cluster.active_nodes
        state.extend(active_nodes)
        node_capacities = self.cluster.node_capacities
        state.extend(node_capacities)
        # anomalous_usage = self.cluster.anomalous_usage
        # state.extend(anomalous_usage)
        response_time = self.cluster.response_time
        state.extend(response_time)
        active_workloads = self.cluster.separate_len_running_task_instances
        state.extend(active_workloads)
        waiting_workloads = self.cluster.separate_len_waiting_task_instances
        state.extend(waiting_workloads)
        active_service_workloads = self.cluster.service_running_task_instances
        state.extend(active_service_workloads)
        metrics_unstarted_workloads = self.cluster.metrics_unstarted_instances
        state.extend(metrics_unstarted_workloads)
        flattened_state = [element for sublist in state for element in (sublist if isinstance(sublist, list) else [sublist])]

        return flattened_state

    def apply_action(self, action):
        print('The selected action was %f' %action)
        if action == 0: 
            return
        if action == 1: #cluster 0 - 1 node scale up
            self.cluster.create_nodes(0, 1)
        if action == 2: #cluster 1 - 1 node scale up
            self.cluster.create_nodes(1, 1)
        if action == 3: #cluster 2 - 1 node scale up
            self.cluster.create_nodes(2, 1)
        """
        SOS here!!!
        i want the actions below to not set the algorithm and call the rl model for the child cluster 
        to decide on the algorithm
        """
        if action == 4: #transfer 2 jobs Near -> Far Edge
            jobs = extract_jobs(self.cluster.child_clusters[0], "max_util", 2)
            receive_jobs(self.cluster.child_clusters[1], "max_util", jobs)
        if action == 5: #transfer 2 jobs Cloud -> Far Edge
            jobs = extract_jobs(self.cluster.child_clusters[2], "max_util", 2)
            receive_jobs(self.cluster.child_clusters[1], "max_util", jobs)
        if action == 6: #transfer 2 jobs Far -> Near Edge
            jobs = extract_jobs(self.cluster.child_clusters[1], "max_util", 2)
            receive_jobs(self.cluster.child_clusters[0], "max_util", jobs)
        if action == 7: #transfer 2 jobs Far -> Cloud Edge
            jobs = extract_jobs(self.cluster.child_clusters[1], "max_util", 2)
            receive_jobs(self.cluster.child_clusters[2], "max_util", jobs)
        if action == 8: #transfer 2 jobs Cloud -> Near Edge
            jobs = extract_jobs(self.cluster.child_clusters[2], "max_util", 2)
            receive_jobs(self.cluster.child_clusters[0], "max_util", jobs)
        if action == 9: #reallocate 5 workloads inside Near Edge
            reallocate_cluster_workloads(self.cluster.child_clusters[0], "max_util", 10)
        if action == 10: #reallocate 5 workloads inside Far Edge
            reallocate_cluster_workloads(self.cluster.child_clusters[1], "max_util", 10)
        if action == 11: #reallocate 5 workloads inside Cloud 
            reallocate_cluster_workloads(self.cluster.child_clusters[2], "max_util", 10)
        # if action == 12: #cluster 0 - 1 node scale down
        #     self.cluster.remove_nodes(0, 1)
        # if action == 13: #cluster 1 - 1 node scale down
        #     self.cluster.remove_nodes(1, 1)
        # if action == 14: #cluster 2 - 1 node scale down
        #     self.cluster.remove_nodes(2, 1)
        