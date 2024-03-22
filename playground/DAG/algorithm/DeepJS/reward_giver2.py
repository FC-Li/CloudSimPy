import math

class RewardGiver():
    def __init__(self, cluster):
        self.cluster = cluster

    def get_overall_reward(self):
        reward = 0
        util = self.utilization()
        response_times = self.response_time()
        transmit_delays = self.transmit_delays()
        reward += util
        reward += response_times
        # reward += self.anomaly()
        reward += transmit_delays
        print('util reward is %f, response_time reward is %f and transmit delays reawrd is %f'\
        % (util, response_times, transmit_delays))
        return reward

    def utilization(self):
        avg_sum = self.cluster.avg_usage  
        reward = avg_sum
        return reward

    def response_time(self):
        RTmin = 0
        RTmax_batch = 5000
        RTmax_service = 2000
        sum = 0
      
        service_response_times, batch_response_times = self.cluster.response_times
        for rt in service_response_times:
            if (RTmin <= rt and RTmax_service > rt):
                sum += 1
            else:
                sum += math.exp(-((rt - RTmax_service) / RTmax_service))
        for rt in batch_response_times:
            if (RTmin <= rt and RTmax_batch > rt):
                sum += 0.5
            else:
                sum += math.exp(-((rt - RTmax_batch) / RTmax_batch))
        if len(service_response_times) + len(batch_response_times) == 0:
            return 0
        reward = sum / (len(service_response_times) + len(batch_response_times))
        return reward

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
        print('edge instances len is %f and cloud job instances len is %f'\
        % (len_edge_task_instances, len_cloud_task_instances))
        return reward
        
        
        
        
                
            
