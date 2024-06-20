import subprocess
import sys
import os

# List of Python scripts to run
script = 'run_agent.py'

scripts_directory = '/Users/aris/Documents/GitHub/CloudSimPy/playground/auxiliary'
script_path = os.path.join(scripts_directory, script)

script2 = 'main-single-process.py'

scripts_directory2 = '/Users/aris/Documents/GitHub/CloudSimPy/playground/DAG/launch_scripts'
script_path2 = os.path.join(scripts_directory2, script2)

script_arguments3 = [
    ['1', 'FirstFit', 'all_updated_0.4_e', '0.00001', '6', 'MSE', 'ReLU', '0.4', 'True'],
]

script_arguments = [
    ['1', 'FirstFit', 'all_updated_var_e', '0.00001', '6', 'MSE', 'ReLU', '0.4', 'True'],
]

script_arguments10 = [
    ['0', 'BestFit', 'all_updated', '0.00001', '6', 'MSE', 'ReLU', '0.4', 'False']
]

lower_bound = 26

# for args in script_arguments:


    # for _ in range(15):

    #     # Execute the script using subprocess
    #     print(f"Running script: {script2} with arguments: {args}")
    #     subprocess.run([script_path2, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8]])

    # for i in range(5):
    #     # Execute the script using subprocess
    #     print(f"Running script: {script} with arguments: {args}")
    #     subprocess.run([script_path, args[2], args[3], args[4], args[5], args[6], str(lower_bound), 'False'])

    # subprocess.run([script_path2, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], 'False', '2000', '10'])

#     # lower_bound += 25

#     subprocess.run([script_path2, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], 'False', '4000', '10'])

#     subprocess.run([script_path2, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], 'False', '0', '10'])

# for args in script_arguments10:

# #     subprocess.run([script_path2, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], 'False', '0', '10'])

#     subprocess.run([script_path2, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], 'False', '0', '10'])


lower_bound = 173

for args in script_arguments3:
    for _ in range(1):
        
        # for _ in range(25):
        #     # Execute the script using subprocess
        #     print(f"Running script: {script2} with arguments: {args}")
        #     subprocess.run([script_path2, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], '2500', '1'])
    # for i in range(4):
        # Execute the script using subprocess
        print(f"Running script: {script} with arguments: {args}")
        subprocess.run([script_path, args[2], args[3], args[4], args[5], args[6], str(lower_bound), 'False'])

        lower_bound += 25

        # subprocess.run([script_path2, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], 'False', '2000', '10'])

        # subprocess.run([script_path2, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], 'False', '4000', '10'])

        # subprocess.run([script_path2, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], 'False', '0', '10'])

print("All testing scripts have been executed for constant e.")

lower_bound = 177

for args in script_arguments:
    for _ in range(1):
        
        for _ in range(25):
            # Execute the script using subprocess
            print(f"Running script: {script2} with arguments: {args}")
            subprocess.run([script_path2, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], '2500', '1'])
        for i in range(2):
            # Execute the script using subprocess
            print(f"Running script: {script} with arguments: {args}")
            subprocess.run([script_path, args[2], args[3], args[4], args[5], args[6], str(lower_bound), 'False'])

        lower_bound += 25

        # subprocess.run([script_path2, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], 'False', '2000', '10'])

        # subprocess.run([script_path2, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], 'False', '4000', '10'])

        # subprocess.run([script_path2, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], 'False', '0', '10'])

print("All testing scripts have been executed for constant e.")

# lower_bound = 51

# script_arguments = [
#     ['1', 'FirstFit', 'all_updated_var_e', '0.00001', '6', 'MSE', 'ReLU', '0.7', 'True'],
#     ['1', 'FirstFit', 'all_updated_var_e', '0.00001', '6', 'MSE', 'ReLU', '0.5', 'True'],
#     ['1', 'FirstFit', 'all_updated_var_e', '0.00001', '6', 'MSE', 'ReLU', '0.4', 'True'],
#     ['1', 'FirstFit', 'all_updated_var_e', '0.00001', '6', 'MSE', 'ReLU', '0.3', 'True'],
#     ['1', 'FirstFit', 'all_updated_var_e', '0.00001', '6', 'MSE', 'ReLU', '0.2', 'True']]

# for args in script_arguments:

#     if float(args[7]) < 0.5:
#         for _ in range(25):
#             # Execute the script using subprocess
#             print(f"Running script: {script2} with arguments: {args}")
#             subprocess.run([script_path2, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8]])

#         for i in range(15):
#             # Execute the script using subprocess
#             print(f"Running script: {script} with arguments: {args}")
#             subprocess.run([script_path, args[2], args[3], args[4], args[5], args[6], str(lower_bound), 'False'])

#     lower_bound += 25

#     if float(args[7]) < 0.5:

#         subprocess.run([script_path2, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], 'False'])

#     print("I tested the model for the variable", args[7])

# print("All testing scripts have been executed for variable e.")

# script_arguments3 = [
#     ['1', 'FirstFit', 'all_updated_0.4_e', '0.00001', '6', 'MSE', 'ReLU', '0.4', 'True'],
# ]

# # Arguments to pass to the Python scripts
# script_arguments = [
#     ['all_updated_var_e', '0.00001', '6', 'MSE', 'ReLU'],  # Arguments for script1.py
# ]
#     ['all', '0.00001', '6', 'MSE', 'ReLU'],
#     ['all', '0.000005', '6', 'MSE', 'ReLU'],
#     ['all', '0.0001', '5', 'MSE', 'ReLU'],
#     ['all', '0.00001', '5', 'MSE', 'ReLU'],
#     ['all', '0.000005', '5', 'MSE', 'ReLU'],
#     ['all', '0.0001', '6', 'Huber', 'ReLU'],  # Arguments for script1.py
#     ['all', '0.00001', '6', 'Huber', 'ReLU'],
#     ['all', '0.000005', '6', 'Huber', 'ReLU'],
#     ['all', '0.0001', '5', 'Huber', 'ReLU'],
#     ['all', '0.00001', '5', 'Huber', 'ReLU'],
#     ['all', '0.000005', '5', 'Huber', 'ReLU'],
#     ['all', '0.0001', '6', 'MSE', 'LeakyReLU'],  # Arguments for script1.py
#     ['all', '0.00001', '6', 'MSE', 'LeakyReLU'],
#     ['all', '0.000005', '6', 'MSE', 'LeakyReLU'],
#     ['all', '0.0001', '5', 'MSE', 'LeakyReLU'],
#     ['all', '0.00001', '5', 'MSE', 'LeakyReLU'],
#     ['all', '0.000005', '5', 'MSE', 'LeakyReLU']
# ]
# script_arguments = [
# #     # ['all', '0.00001', '6', 'MSE', 'ReLU'],  # Arguments for script1.py
# #     # ['all', '0.00001', '6', 'MSE', 'LeakyReLU'],
# #     # ['util', '0.00001', '6', 'MSE', 'ReLU'],  # Arguments for script1.py
# #     # ['util', '0.00001', '6', 'MSE', 'LeakyReLU'],
#     ['response_time', '0.00001', '6', 'MSE', 'ReLU']
#     # ['response_time', '0.00001', '6', 'Huber', 'ReLU'],
# ]


# # List of Python scripts to run
# script2 = 'main-single-process.py'

# scripts_directory2 = '/Users/aris/Documents/GitHub/CloudSimPy/playground/DAG/launch_scripts'
# script_path2 = os.path.join(scripts_directory2, script2)

# # Arguments to pass to the Python scripts
# script_arguments2 = [
#     # ['0', 'FirstFit', 'all', '0.00001', '6', 'MSE', 'ReLU'],
#     # ['0', 'BestFit', 'all', '0.00001', '6', 'MSE', 'ReLU'],
#     ['1', 'FirstFit', 'all_updated_var_e', '0.00001', '6', 'MSE', 'ReLU', '0.7'],
#     ['1', 'FirstFit', 'all_updated_var_e', '0.00001', '6', 'MSE', 'ReLU', '0.5'],
#     ['1', 'FirstFit', 'all_updated_var_e', '0.00001', '6', 'MSE', 'ReLU', '0.4'],
#     ['1', 'FirstFit', 'all_updated_var_e', '0.00001', '6', 'MSE', 'ReLU', '0.3'],
#     ['1', 'FirstFit', 'all_updated_var_e', '0.00001', '6', 'MSE', 'ReLU', '0.2']
#     # ['1', 'FirstFit', 'all', '0.00001', '6', 'MSE', 'LeakyReLU']]
#     # ['1', 'FirstFit', 'util', '0.00001', '6', 'MSE', 'ReLU'],
#     # ['1', 'FirstFit', 'util', '0.00001', '6', 'MSE', 'LeakyReLU'],
#     # ['1', 'FirstFit', 'response_time', '0.00001', '6', 'Huber', 'ReLU'],
#     # ['1', 'FirstFit', 'response_time', '0.00001', '6', 'MSE', 'ReLU']
# ]

# # Iterate over each script and run it
# for args in script_arguments2:
# # for script, args in zip(scripts_to_run, script_arguments):

#     for _ in range(25):

#         # Execute the script using subprocess
#         print(f"Running script: {script2} with arguments: {args}")
#         subprocess.run([script_path2, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7]])

# print("All testing scripts have been executed.")
