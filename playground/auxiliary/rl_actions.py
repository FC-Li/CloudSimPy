import os 

from playground.DAG.utils.csv_reader import CSVReader

def RLactions():
    
    job2_csv = os.path.join("DAG", "jobs_files", "job2.csv")
    csv_reader = CSVReader(job2_csv)
    jobs_configs2 = csv_reader.generate(0, 9)

    return jobs_configs2