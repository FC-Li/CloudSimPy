def remove_delays(submit_time, clock):
    i = int(submit_time)
    lost_time = 0.0
    while(i <= int(clock)):
        if i % 300 == 0 and i != 0:
            lost_time += 301.0 # subtract the time lost inside the pause event
            i += 300
        else: i += 1
    response_time = clock - submit_time - lost_time
    print(submit_time, clock)
    return response_time
