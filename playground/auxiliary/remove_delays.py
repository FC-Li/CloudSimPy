def remove_delays(submit_time, clock):
    i = int(task.job.job_config.submit_time)
    while(i <= int(clock)):
        if i % 100 == 0 and i != 0:
            lost_time += 301 # subtract the time lost inside the pause event
            i += 301
        else: i += 1
    response_time = clock - task.job.job_config.submit_time - lost_time
    return response_time
