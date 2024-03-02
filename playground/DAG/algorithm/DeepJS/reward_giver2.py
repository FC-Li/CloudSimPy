import math

class RewardGiver(cluster):
    self.cluster = cluster

    def utilization():
        avg_sum = self.cluster.avg_usage  
        reward = 1 - avg_sum
        return reward

    def response_time():
        RTmin = 0
        RTmax_batch = 10000
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
        reward = reward / (len(service_response_times) + len(batch_response_times))
        return reward

    def anomaly():
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

    def transmit_delays():
        sum = 0
        len_task_instances = self.cluster.len_all_task_instances
        delays = self.cluster.transmit_delays
        sum += delays[0]
        sum -= delays[2]
        reward = sum / len_task_instances
        return reward
        
        
        
        
                
            
