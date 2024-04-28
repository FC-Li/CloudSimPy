import subprocess
import sys
import os

sys.path.append('..')

# Define the number of times to run the script
num_runs = 50

# Path to the directory containing the Python script
script_directory = 'DAG/launch_scripts'

# Name of the Python script to run
script_name = 'main-single-process.py'

script_path = os.path.join(script_directory, script_name)

# Loop to run the script multiple times
for _ in range(num_runs):    
    # Run the script using subprocess
    subprocess.run(['python3', script_path])
