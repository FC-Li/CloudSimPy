import pandas as pd
import numpy as np
import os

def modify_submit_time(file_path, modified_file_path):
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Identify unique submit times and the incremental difference
    unique_times = df.iloc[:, 0].unique()
    time_diff = 2  # Increment each unique time by 2
    
    # Create a mapping of original times to modified times
    time_mapping = {time: time + i * time_diff for i, time in enumerate(sorted(unique_times))}
    
    # Apply the mapping to modify the submit times in the DataFrame
    df.iloc[:, 0] = df.iloc[:, 0].map(time_mapping)
    
    # Save the modified DataFrame to a new CSV file
    df.to_csv(modified_file_path, index=False)

# Assuming you've loaded the CSV files into pandas DataFrames named job_df and jobs_df
# Load your CSV files
jobs_csv = os.path.join("DAG", "jobs_files", "modified_jobs.csv")
# Save the modified jobs.csv to a new file
modified_jobs_csv_path = 'DAG/jobs_files/jobs.csv'

# Call the function
modify_submit_time(jobs_csv, modified_jobs_csv_path)

print("File has been modified and saved as:", modified_jobs_csv_path)
