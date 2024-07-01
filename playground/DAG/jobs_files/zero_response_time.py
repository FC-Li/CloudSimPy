import pandas as pd
import os

def set_first_column_to_zero(file_path, modified_file_path):
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Set the first column (assumed to be 'submit_time' or equivalent) to 0 for all rows
    df.iloc[:, 0] = 0
    
    # Save the modified DataFrame to a new CSV file
    df.to_csv(modified_file_path, index=False)

# Define the paths to your input and output files
file_path = 'DAG/jobs_files/modified_jobs.csv'  # Update this to your actual file path
modified_file_path = 'DAG/jobs_files/jobs_zero.csv'  # Update this for the output file

# Call the function to modify the first column to 0
set_first_column_to_zero(file_path, modified_file_path)

print(f"File has been modified and saved as: {modified_file_path}")
