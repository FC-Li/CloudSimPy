import math

class RewardGiver():
    def __init__(self, cluster):
        self.cluster = cluster
        self.flag = 1
        self.cost_flag = 1
        self.first_time = 1
        self.res_flag = 1
        self.last_util = None
        self.last_cost = None
        self.response_time_threshold = 2500
        self.last_cnt_running = 0
        self.last_response_time_reward = None
        self.crossed_time_threshold = 0

    def get_overall_reward(self, old_reward_list):
        cnt = 0
        self.flag = 0
        self.res_flag = 1
        self.cost_flag = 0
        if (len(self.cluster.not_started_task_instances) == 0):
            print("i have no unstarted workloads")
            if self.first_time:
                self.first_time = 0
            else:
                self.flag = 0
        else:
            new_flag = self.flag
            check = 0
            for sep_len in (self.cluster.separate_len_unscheduled_task_instances):
                if (sep_len == 0):
                    check = 1
                    self.cost_flag = 1
                    if self.first_time:
                        self.first_time = 0
                    else:
                        self.flag = 1 #only count the util reward if there are not fully used resources
                    break
            if check == 0:
                self.first_time = 1
            # if (self.first_time and new_flag):
            #     self.flag = 1
        list_unfinished = self.cluster.separate_len_0_05_1_unscheduled_task_instances
        list_capacities = self.cluster.nodes_num_usage
        if (list_unfinished[0] == 0.5 and self.first_time == 0):
            if list_capacities[0] != 1:
                self.flag = 0
            elif (list_unfinished[1] == 0.5):
                if list_capacities[1] != 1:
                    self.flag = 0
                # elif (list_unfinished[2] == 0.5):
                #     if list_capacities[2] != 1:
                #         self.flag = 0

        if (self.cluster.overall_response_time < (self.response_time_threshold / 2 )):
            print("yes")
            self.res_flag = 0
            self.crossed_time_threshold = 0
        else:
            if self.crossed_time_threshold == 0:
                self.crossed_time_threshold = 1
            elif self.crossed_time_threshold == 1:
                self.crossed_time_threshold = 2

        reward = 0
        old_reward = old_reward_list[0]
        previous_sign = old_reward_list[2]
        transmit_delays = self.transmit_delays()
        if (self.flag == 1):
            util = self.last_util = self.utilization()
            reward += (0.2 * util)      
        else:
            if (self.last_util == None):
                self.last_util = self.utilization()
            util = self.last_util
            reward += (0.2 * util)
        # self.res_flag = 1
        if self.res_flag == 1:
            response_times = self.last_response_time_reward = self.response_time()
            reward += (1.5 * response_times)
        else:
            if (self.last_response_time_reward == None):
                self.last_response_time_reward = self.response_time()
            response_times = self.last_response_time_reward
            reward += (1.5 * response_times)
        # if (self.cost_flag == 1):
        #     cost = self.last_cost = self.monetary_cost()
        #     reward += (0.15 * cost)      
        # else:
        #     if (self.last_cost == None):
        #         self.last_cost = self.monetary_cost()
        #     cost = self.last_cost
        #     reward += (0.15 * cost)
            
        monetary_cost = self.monetary_cost()
        reward += (0.1 * monetary_cost)
        # reward += self.anomaly()
        # reward += (0.25 * transmit_delays)
        print('util reward is %f, response_time reward is %f and transmit delays reward is %f '\
        'and monetary reward is %f' % ((0.5 * util), (1.5 * response_times), (0.1 * transmit_delays), (0.1 * monetary_cost)))
        print(reward)
        if reward == 0 and old_reward == 0:
            a = 0
        a = reward / (reward + old_reward)

        if self.crossed_time_threshold == 1:
            return reward, 0, "+"

        if old_reward == 0:
            return reward, 0, "+"
        if (self.flag == 0):
            limits = [0.4999, 0.497, 0.5001, 0.5005, 0.501, 0.507]
        elif (self.res_flag == 0):
            limits = [0.4999, 0.497, 0.5001, 0.502, 0.503, 0.6]
        else:
            limits = [0.499, 0.491, 0.501, 0.509, 0.52, 0.54]
        if previous_sign == "-":
            if (reward < old_reward):
                if a > limits[0]:
                    overall_reward = 0
                elif a < limits[1]:
                    overall_reward = -2
                else:
                    overall_reward = -1
            else:
                if a < limits[2]:
                    overall_reward = 0
                elif a >= limits[5]:
                    overall_reward = 3    
                elif a >= limits[4]:
                    overall_reward = 2
                elif a >= limits[3]:
                    overall_reward = 1
                else:
                    overall_reward = 0.5
        elif previous_sign == "+":
            if (reward < old_reward):
                if a > limits[0]:
                    overall_reward = 0
                elif a < limits[1]:
                    overall_reward = -1
                else:
                    overall_reward = -0.5
            else:
                if a < limits[2]:
                    overall_reward = 0
                elif a >= limits[5]:
                    overall_reward = 5  
                elif a >= limits[4]:
                    overall_reward = 3
                elif a >= limits[3]:
                    overall_reward = 2
                else:
                    overall_reward = 1
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
        RTmax_batch = self.response_time_threshold
        RTmax_service = self.response_time_threshold
        sum1 = sum2 = sum3 = 0
        cnt = cnt_running = cnt_waiting = 0
      
        service_response_instances, batch_response_instances = self.cluster.response_times
        for instance in service_response_instances:
            flag = 0
            instance_rew = 0
            if (instance.running == True and instance.has_finished == False):
                flag = 1
                cnt_running += 1
            if instance.has_finished:
                cnt += 1
            # max_threshold = instance.task.task_config.response_time_threshold
            rt = instance.response_time
            if (RTmin <= rt and RTmax_batch > rt):
                instance_rew = 1
            else:
                instance_rew = math.exp(-((rt - RTmax_batch) / RTmax_batch))
                if instance_rew < 0:
                    instance_rew = 0
            if (flag == 1 and (instance.machine.node.topology == 0)):
                instance_rew *= 8
                sum3 += instance_rew
            elif (flag == 1 and (instance.machine.node.topology == 1)):
                instance_rew *= 4
                sum3 += instance_rew
            elif (flag == 1 and (instance.machine.node.topology == 2)):
                instance_rew *= 2
                sum3 += instance_rew
            else:
                sum1 += instance_rew
                cnt_waiting += 1
        for instance in batch_response_instances:
            flag = 0
            instance_rew = 0
            if (instance.running == True and instance.has_finished == False):
                flag = 1
                cnt_running += 1
            if instance.has_finished:
                cnt += 1
            rt = instance.response_time
            if (RTmin <= rt and RTmax_batch > rt):
                instance_rew = 1
            else:
                instance_rew = math.exp(-((rt - RTmax_batch) / RTmax_batch))
                if instance_rew < 0:
                    instance_rew = 0
            if (flag == 1 and (instance.machine.node.topology == 0)):
                instance_rew *= 8
                sum3 += instance_rew
            elif (flag == 1 and (instance.machine.node.topology == 1)):
                instance_rew *= 4
                sum3 += instance_rew
            elif (flag == 1 and (instance.machine.node.topology == 2)):
                instance_rew *= 2
                sum3 += instance_rew
            else:
                sum1 += instance_rew
                cnt_waiting += 1
        unfinished_len = len(service_response_instances) + len(batch_response_instances)
        if unfinished_len == 0:
            reward1 = 0
        else:
            if self.last_cnt_running == 0:
                reward1 = sum1 / unfinished_len
            else:
                # print(f"The last unfinished instances were {self.last_unfinished_len}"\
                # f"and now they are {unfinished_len}")
                reward1 = ((sum3 +  sum1) / (self.last_cnt_running + cnt_waiting))
        self.last_cnt_running = cnt_running

        service_finished_instances, batch_finished_instances = self.cluster.finished_type_response_times
        # print(len(service_finished_instances))
        service_finished_instances.extend(self.cluster.deleted_nodes_times[0])
        # print(len(service_finished_instances))
        batch_finished_instances.extend(self.cluster.deleted_nodes_times[1])
        for instance in service_finished_instances:
            # max_threshold = instance.task.task_config.response_time_threshold
            rt = instance.response_time
            if (RTmin <= rt and RTmax_batch > rt):
                sum2 += 1
            else:
                sum2 += math.exp(-((rt - RTmax_batch) / RTmax_batch))
        for instance in batch_finished_instances:
            # max_threshold = instance.task.task_config.response_time_threshold
            rt = instance.response_time
            if (RTmin <= rt and RTmax_batch > rt):
                sum2 += 1
            else:
                sum2 += math.exp(-((rt - RTmax_batch) / RTmax_batch))
        finished_len = len(service_finished_instances) + len(batch_finished_instances)
        if finished_len == 0:
            reward2 = 0
        else:
            reward2 = sum2 / finished_len
        if (unfinished_len == 0):
            return reward2
        else:
            a = unfinished_len / (unfinished_len + finished_len)
            # a += 0.2
            # if a > 1:
            #     a = 1
        # sum3 = self.cluster.finished_task_instances
        # print(f'The number of finished transfered workloads is {cnt}')
        # print(f'The num of unfinished instances is {unfinished_len}, the sum of running '\
        # f'instances is {cnt_running} and finished is {finished_len} and generally {sum3}')
        # print(f'The sum of unfinished instances is {sum1}, the sum of running '\
        # f'and finished from the reward func is {sum2}')
        print(reward1, sum1, reward2, sum2, a)
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
        # pricing = [0.305, 0.24, 0.1645]
        pricing = [0.1, 0.05, 0.02]
        # max_machines = [141, 192, 282]  # Max machines for each level
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

        
                
        
        
        
        
                
            
