import subprocess
import sys
import os

# List of Python scripts to run
script = 'run_agent.py'

scripts_directory = '/Users/aris/Documents/GitHub/CloudSimPy/playground/auxiliary'
script_path = os.path.join(scripts_directory, script)

# # Arguments to pass to the Python scripts
# script_arguments = [
#     ['all', '0.00001', '6', 'MSE', 'ReLU'],  # Arguments for script1.py
# ]
# #     ['all', '0.00001', '6', 'MSE', 'ReLU'],
# #     ['all', '0.000005', '6', 'MSE', 'ReLU'],
# #     ['all', '0.0001', '5', 'MSE', 'ReLU'],
# #     ['all', '0.00001', '5', 'MSE', 'ReLU'],
# #     ['all', '0.000005', '5', 'MSE', 'ReLU'],
# #     ['all', '0.0001', '6', 'Huber', 'ReLU'],  # Arguments for script1.py
# #     ['all', '0.00001', '6', 'Huber', 'ReLU'],
# #     ['all', '0.000005', '6', 'Huber', 'ReLU'],
# #     ['all', '0.0001', '5', 'Huber', 'ReLU'],
# #     ['all', '0.00001', '5', 'Huber', 'ReLU'],
# #     ['all', '0.000005', '5', 'Huber', 'ReLU'],
# #     ['all', '0.0001', '6', 'MSE', 'LeakyReLU'],  # Arguments for script1.py
# #     ['all', '0.00001', '6', 'MSE', 'LeakyReLU'],
# #     ['all', '0.000005', '6', 'MSE', 'LeakyReLU'],
# #     ['all', '0.0001', '5', 'MSE', 'LeakyReLU'],
# #     ['all', '0.00001', '5', 'MSE', 'LeakyReLU'],
# #     ['all', '0.000005', '5', 'MSE', 'LeakyReLU']
# # ]
# script_arguments = [
# #     # ['all', '0.00001', '6', 'MSE', 'ReLU'],  # Arguments for script1.py
# #     # ['all', '0.00001', '6', 'MSE', 'LeakyReLU'],
# #     # ['util', '0.00001', '6', 'MSE', 'ReLU'],  # Arguments for script1.py
# #     # ['util', '0.00001', '6', 'MSE', 'LeakyReLU'],
#     ['response_time', '0.00001', '6', 'MSE', 'ReLU']
#     # ['response_time', '0.00001', '6', 'Huber', 'ReLU'],
# ]

# # Iterate over each script and run it
# for args in script_arguments:
# # for script, args in zip(scripts_to_run, script_arguments):
    
#     for i in range(10):
#         # Execute the script using subprocess
#         print(f"Running script: {script} with arguments: {args}")
#         subprocess.run([script_path, args[0], args[1], args[2], args[3], args[4]])

# print("All agent training scripts have been executed.")

# List of Python scripts to run
script2 = 'main-single-process.py'

scripts_directory2 = '/Users/aris/Documents/GitHub/CloudSimPy/playground/DAG/launch_scripts'
script_path2 = os.path.join(scripts_directory2, script2)

# Arguments to pass to the Python scripts
script_arguments2 = [
    # ['0', 'FirstFit', 'all', '0.00001', '6', 'MSE', 'ReLU'],
    # ['0', 'BestFit', 'all', '0.00001', '6', 'MSE', 'ReLU'],
    ['1', 'FirstFit', 'all_updated_0.4_e', '0.00001', '6', 'MSE', 'ReLU']
    # ['1', 'FirstFit', 'all', '0.00001', '6', 'MSE', 'LeakyReLU']]
    # ['1', 'FirstFit', 'util', '0.00001', '6', 'MSE', 'ReLU'],
    # ['1', 'FirstFit', 'util', '0.00001', '6', 'MSE', 'LeakyReLU'],
    # ['1', 'FirstFit', 'response_time', '0.00001', '6', 'Huber', 'ReLU'],
    # ['1', 'FirstFit', 'response_time', '0.00001', '6', 'MSE', 'ReLU']
]

# Iterate over each script and run it
for args in script_arguments2:
# for script, args in zip(scripts_to_run, script_arguments):

    for _ in range(100):
        
        # Execute the script using subprocess
        print(f"Running script: {script2} with arguments: {args}")
        subprocess.run([script_path2, args[0], args[1], args[2], args[3], args[4], args[5], args[6]])

print("All testing scripts have been executed.")
