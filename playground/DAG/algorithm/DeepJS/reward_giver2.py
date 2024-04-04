import math

class RewardGiver():
    def __init__(self, cluster):
        self.cluster = cluster

    def get_overall_reward(self, old_reward):
        reward = 0
        util = self.utilization()
        response_times = self.response_time()
        transmit_delays = self.transmit_delays()
        monetary_cost = self.monetary_cost()
        reward += util
        reward += response_times
        reward += monetary_cost
        # reward += self.anomaly()
        # reward += (0.25 * transmit_delays)
        print('util reward is %f, response_time reward is %f and transmit delays reward is %f '\
        'and monetary cost is %f' % (util, response_times, (0.25 * transmit_delays), monetary_cost))
        print(reward)
        if (old_reward != 0):
            print((4 * reward) + (50 * (reward - old_reward)))
            return reward, (4 * reward) + (50 * (reward - old_reward))
        else:
            print(4 * reward)
            return reward, (4 * reward)

    def utilization(self):
        avg_sum = self.cluster.avg_usage  
        reward = avg_sum
        return reward

    def response_time(self):
        RTmin = 0
        RTmax_batch = 2000
        RTmax_service = 2000
        sum1 = sum2 = 0
      
        service_response_times, batch_response_times = self.cluster.response_times
        for rt in service_response_times:
            if (RTmin <= rt and RTmax_service > rt):
                sum1 += 1
            else:
                sum1 += math.exp(-((rt - RTmax_service) / RTmax_service))
        for rt in batch_response_times:
            if (RTmin <= rt and RTmax_batch > rt):
                sum1 += 0.5
            else:
                sum1 += math.exp(-((rt - RTmax_batch) / RTmax_batch))
        unfinished_len = len(service_response_times) + len(batch_response_times)
        if unfinished_len == 0:
            reward1 = 0
        else:
            reward1 = sum1 / unfinished_len

        service_finished_instances, batch_finished_instances = self.cluster.finished_type_response_times
        for instance in service_finished_instances:
            if (RTmin <= instance.response_time and RTmax_service > instance.response_time):
                sum2 += 1
            else:
                sum2 += math.exp(-((instance.response_time - RTmax_service) / RTmax_service))
        for instance in batch_finished_instances:
            if (RTmin <= instance.response_time and RTmax_batch > instance.response_time):
                sum2 += 0.5
            else:
                sum2 += math.exp(-((instance.response_time - RTmax_batch) / RTmax_batch))
        finished_len = len(service_finished_instances) + len(batch_finished_instances)
        if finished_len == 0:
            reward2 = 0
        else:
            reward2 = sum2 / finished_len

        if (unfinished_len == 0):
            return reward2
        else:
            a = unfinished_len / (unfinished_len + finished_len)

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
        max_machines = [66, 165, 396]  # Max machines for each level
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

        
                
        
        
        
        
                
            
