import pandas as pd
import numpy as np
import os

# Assuming you've loaded the CSV files into pandas DataFrames named job_df and jobs_df
# Load your CSV files
jobs_csv = os.path.join("DAG", "jobs_files", "backup_jobs.csv")

jobs_df = pd.read_csv(jobs_csv)

# Set response_time to 0 for all rows in jobs.csv
jobs_df['response_time'] = 0

# Update task_id in jobs.csv to only include the first number before "_"
jobs_df['task_id'] = jobs_df['task_id'].apply(lambda x: x.split('_')[0])

# Randomly assign values in the range 5 to 50 to 'instances_num' column
jobs_df['instances_num'] = np.random.randint(5, 51, size=len(jobs_df))

# Assign random type 1 or 2 to each unique job_id in jobs.csv, ensuring consistency within job_ids
unique_job_ids = jobs_df['job_id'].unique()
job_id_to_type = {job_id: np.random.choice([1, 2]) for job_id in unique_job_ids}
jobs_df['type'] = jobs_df['job_id'].apply(lambda job_id: job_id_to_type[job_id])

# Save the modified jobs.csv to a new file
modified_jobs_csv_path = 'DAG/jobs_files/modified_jobs.csv'
jobs_df.to_csv(modified_jobs_csv_path, index=False)

# Keep only the first 50 rows
df_first_50 = jobs_df.head(5000)
# Save the modified DataFrame to a new CSV file
df_first_50.to_csv('DAG/jobs_files/small_modified_jobs.csv', index=False)

print(f"Modified jobs.csv saved to {modified_jobs_csv_path}")
