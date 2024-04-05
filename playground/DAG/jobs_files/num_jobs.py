import pandas as pd
import numpy as np
import os

# Assuming you've loaded the CSV files into pandas DataFrames named job_df and jobs_df
# Load your CSV files
jobs_csv = os.path.join("DAG", "jobs_files", "jobs_zero.csv")

jobs_df = pd.read_csv(jobs_csv)

# Save the modified jobs.csv to a new file
modified_jobs_csv_path = 'DAG/jobs_files/modified_jobs.csv'
jobs_df.to_csv(modified_jobs_csv_path, index=False)

# Keep only the first 50 rows
df_first_50 = jobs_df.head(600)
# Save the modified DataFrame to a new CSV file
df_first_50.to_csv('DAG/jobs_files/small_modified_jobs.csv', index=False)

print(f"Modified jobs.csv saved to {modified_jobs_csv_path}")
