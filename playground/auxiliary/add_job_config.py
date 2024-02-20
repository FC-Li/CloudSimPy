import os 

from core.runbroker import RunBroker
from playground.DAG.utils.csv_reader import CSVReader

def add_job_config(simulation, broker):
    
    job2_csv = os.path.join("DAG", "jobs_files", "job2.csv")
    csv_reader = CSVReader(job2_csv, simulation.env.now)
    jobs_configs2 = csv_reader.generate(0, 9)

    task_broker2 = broker(simulation.env, jobs_configs2)
    new_task_broker = RunBroker(simulation.env, simulation, task_broker2)
    new_task_broker.run()

    return jobs_configs2