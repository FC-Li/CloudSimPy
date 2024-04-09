import math

class RewardGiver():
    def __init__(self, cluster):
        self.cluster = cluster
        self.flag = 1
        self.last_util = None

    def get_overall_reward(self, old_reward_list):
        cnt = 0
        self.flag = 1
        if (len(self.cluster.not_started_task_instances) == 0):
            print("i have no unstarted workloads")
            self.flag = 0
        if self.flag == 1:
            self.flag = 0
            for sep_len in (self.cluster.separate_len_unscheduled_task_instances):
                if (sep_len == 0):
                    self.flag = 1 #only count the util reward if there are not fully used resources
                    break
        reward = 0
        old_reward = old_reward_list[0]
        previous_sign = old_reward_list[2]
        response_times = self.response_time()
        transmit_delays = self.transmit_delays()
        monetary_cost = self.monetary_cost()
        if (self.flag == 1):
            reward += (0.5 * self.utilization())
            util = self.last_util = self.utilization()
        else:
            if (self.last_util == None):
                self.last_util = self.utilization()
            util = self.last_util
            reward += (0.5 * util)
        reward += (1.5 * response_times)
        reward += monetary_cost
        # reward += self.anomaly()
        # reward += (0.25 * transmit_delays)
        print('util reward is %f, response_time reward is %f and transmit delays reward is %f '\
        'and monetary reward is %f' % ((0.5 * util), (1.5 * response_times), (0.25 * transmit_delays), monetary_cost))
        print(reward)
        a = reward / (reward + old_reward)
        if old_reward == 0:
            return reward, 0, "+"
        if reward > 1.15:
            limits = [0.497, 0.48, 0.503, 0.52]
        else:
            limits = [0.499, 0.48, 0.501, 0.52]
        if previous_sign == "-":
            if (reward < old_reward):
                if a > limits[0]:
                    overall_reward = 0
                elif a < limits[1]:
                    overall_reward = -20
                else:
                    overall_reward = -10
            else:
                if a < limits[2]:
                    overall_reward = 0
                elif a >= limits[3]:
                    overall_reward = 10
                else:
                    overall_reward = 5
        elif previous_sign == "+":
            if (reward < old_reward):
                if a > limits[0]:
                    overall_reward = 0
                elif a < limits[1]:
                    overall_reward = -10
                else:
                    overall_reward = -5
            else:
                if a < limits[2]:
                    overall_reward = 0
                elif a >= limits[3]:
                    overall_reward = 20
                else:
                    overall_reward = 10
        if (reward < old_reward):
            sign = "-"
        else:
            sign = "+"
        print(a, overall_reward, sign)
        return reward, overall_reward, sign
        # if (old_reward != 0):
        #     print((4 * reward) + (50 * (reward - old_reward)))
        #     return reward, (4 * reward) + (50 * (reward - old_reward))
        # else:
        #     print(4 * reward)
        #     return reward, (4 * reward)

    def utilization(self):
        avg_sum = self.cluster.avg_usage  
        reward = avg_sum
        return reward

    def response_time(self):
        RTmin = 0
        RTmax_batch = 500
        RTmax_service = 500
        sum1 = sum2 = 0
      
        service_response_instances, batch_response_instances = self.cluster.response_times
        for instance in service_response_instances:
            max_threshold = instance.task.task_config.response_time_threshold
            rt = instance.response_time
            if (RTmin <= rt and max_threshold > rt):
                sum1 += 1
            else:
                sum1 += math.exp(-((rt - max_threshold) / max_threshold))
        for instance in batch_response_instances:
            max_threshold = instance.task.task_config.response_time_threshold
            rt = instance.response_time
            if (RTmin <= rt and max_threshold > rt):
                sum1 += 1
            else:
                sum1 += math.exp(-((rt - max_threshold) / max_threshold))
        unfinished_len = len(service_response_instances) + len(batch_response_instances)
        if unfinished_len == 0:
            reward1 = 0
        else:
            reward1 = sum1 / unfinished_len

        service_finished_instances, batch_finished_instances = self.cluster.finished_type_response_times
        service_finished_instances.extend(self.cluster.deleted_nodes_times[0])
        batch_finished_instances.extend(self.cluster.deleted_nodes_times[1])
        for instance in service_finished_instances:
            max_threshold = instance.task.task_config.response_time_threshold
            rt = instance.response_time
            if (RTmin <= rt and max_threshold > rt):
                sum2 += 1
            else:
                sum2 += math.exp(-((rt - max_threshold) / max_threshold))
        for instance in batch_finished_instances:
            max_threshold = instance.task.task_config.response_time_threshold
            rt = instance.response_time
            if (RTmin <= rt and max_threshold > rt):
                sum2 += 1
            else:
                sum2 += math.exp(-((rt - max_threshold) / max_threshold))
        finished_len = len(service_finished_instances) + len(batch_finished_instances)
        if finished_len == 0:
            reward2 = 0
        else:
            reward2 = sum2 / finished_len

        if (unfinished_len == 0):
            return reward2
        else:
            a = unfinished_len / (unfinished_len + finished_len)
            a += 0.3
            if a > 1:
                a = 1

        return (a * reward1 + (1 - a) * reward2)

    def anomaly(self):
        sum = 0
        tuples = self.cluster.anomaly_update
        for tuple in tuples:
            if tuple[0] == 0 and tuple[1] == 0:
                sum += 1
            elif tuple[0] == 0 and tuple[1] == 1:
                sum -= 1
            elif tuple[0] == 1 and tuple[1] == 0:
                sum += 2
            elif tuple[0] == 1 and tuple[1] == 1:
                sum -= 2
        reward = sum / len(tuples)
        return reward

    def transmit_delays(self):
        len_edge_task_instances = self.cluster.child_clusters[0].len_all_task_instances
        len_cloud_task_instances = self.cluster.child_clusters[2].len_all_task_instances
        len_far_task_instances = self.cluster.child_clusters[1].len_all_task_instances
        delays = self.cluster.transmit_delays
        if len_edge_task_instances == 0:
            sum1 = 0
        else:
            sum1 = delays[0] / len_edge_task_instances
        if len_cloud_task_instances == 0:
            sum2 = 0
        else:
            sum2 = delays[2] / len_cloud_task_instances
        reward = sum1 - sum2

        print('near edge instances len is %f, far edge %f cloud job instances len is %f'\
        % (len_edge_task_instances, len_far_task_instances, len_cloud_task_instances))
        return reward
    
    def monetary_cost(self):
        pricing = [0.056, 0.054, 0.052]
        max_machines = [105, 270, 690]  # Max machines for each level
        bill = []
        machines = 0
        for child in self.cluster.child_clusters:
            cnt = 0
            for node in child.nodes:
                for machine in node.machines:
                    cnt += pricing[child.level]
                    machines += 1
            bill.append(cnt)
        if machines == 0:
            return 0
        total_cost = sum(bill)

        # Calculate the maximum possible cost accounting for different levels
        max_cost = sum([max_machines[i] * pricing[i] for i in range(len(pricing))])


        # Normalize the total cost to be between 0 and 1
        normalized_cost = (total_cost) / (max_cost)  # Adjusted based on your cost calculation

        return (1 - normalized_cost)

        
                
        
        
        
        
                
            
