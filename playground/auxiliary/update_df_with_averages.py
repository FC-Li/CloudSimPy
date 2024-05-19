import matplotlib.pyplot as plt
import os
import pandas as pd

def update_df_with_averages(df, cluster, time):
    new_rows = []  # Initialize an empty list to hold dictionaries of new row data
    
    if cluster.child_clusters is not None:
        for child in cluster.child_clusters:
            averages = cluster.average_metrics_usage  # Assuming this gets you averages for each child
            new_row = {
                'Time': time,
                'Cluster': child.level,
                'CPU': averages[child.level][0],
                'Memory': averages[child.level][1]
                # 'Disk': averages[child.level][2]
            }
            new_rows.append(new_row)
    
    # Convert new_rows to a DataFrame
    new_rows_df = pd.DataFrame(new_rows)
    
    # Use pandas.concat to add the new rows to the original DataFrame
    if not new_rows_df.empty:
        df = pd.concat([df, new_rows_df], ignore_index=True)
    # print(df)
    return df

def calculate_overall_averages(df, cluster):
    averages_df = df.groupby('Cluster').mean()
    capacities = cluster.capacities
    for i in range(len(cluster.child_clusters)):
        # Divide by the respective capacities
        averages_df.loc[i, 'CPU'] /= capacities[i][0]
        averages_df.loc[i, 'Memory'] /= capacities[i][1]
        # averages_df.loc[i, 'Disk'] /= capacities[i][2]

    # return averages_df[['CPU', 'Memory', 'Disk']]
    return averages_df[['CPU', 'Memory']]

def plot_cpu(df):
    for cluster_name in df['Cluster'].unique():
        cluster_df = df[df['Cluster'] == cluster_name]
        plt.plot(cluster_df['Time'], cluster_df['CPU'], label=cluster_name)

    plt.title('Average CPU Usage Over Time by Cluster')
    plt.xlabel('Time')
    plt.ylabel('Average CPU Usage')
    plt.legend()
    plt.show()

def average_type_instances_df(cluster):
    new_rows = []  # Initialize an empty list to hold dictionaries of new row data
    ls = cluster.finished_type_task_instances
    if cluster.child_clusters is not None:
        for i in range(len(cluster.child_clusters)):
            new_row = {
                'Service_job_instances_%': ls[0][i],
                'Batch_job_instances_%': ls[1][i]
            }
            new_rows.append(new_row)
    # Convert new_rows to a DataFrame
    df = pd.DataFrame(new_rows)
    print(df)
    return

def type_instances_response_times_df(cluster):
    new_rows = []  # Initialize an empty list to hold dictionaries of new row data
    ls = cluster.finished_response_times
    if cluster.child_clusters is not None:
        for i in range(len(cluster.child_clusters)):
            new_row = {
                'Service_job_response_times': ls[0],
                'Batch_job_response_times': ls[1]
            }
            new_rows.append(new_row)
    # Convert new_rows to a DataFrame
    df = pd.DataFrame(new_rows)
    print(df)
    return

def instances_response_times_df(cluster):
    new_rows = []  # Initialize an empty list to hold dictionaries of new row data
    ls = cluster.overall_finished_response_times
    if cluster.child_clusters is not None:
        new_row = {
            'Task_Instances_avg_response_times': ls[0],
        }
        new_rows.append(new_row)
    # Convert new_rows to a DataFrame
    df = pd.DataFrame(new_rows)
    print(df)
    return ls[0]

def anomaly_2_step_occurancies_df(cluster):
    new_rows = []  # Initialize an empty list to hold dictionaries of new row data
    ls = cluster.continuous_anomaly
    if cluster.child_clusters is not None:
        for i in range(len(cluster.child_clusters)):
            new_row = {
                'anomaly_%': ls[i],
            }
            new_rows.append(new_row)   
    # Convert new_rows to a DataFrame
    df = pd.DataFrame(new_rows)
    print(df)
    return

def create_and_update_dataframe(values):

    filename = 'data.csv'
    columns = ['System_specs', 'Total_runtime', 'Avg energy consumption cost of machines in $',
    'Overall energy consumption cost of machines in $', 'Avg response time of completed task instances']
    # Create directory if it doesn't exist
    data_dir = '/Users/aris/Documents/GitHub/CloudSimPy/playground/DAG/extracted_data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    filepath = os.path.join(data_dir, filename)

    try:
        # Try to load existing DataFrame from file
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        # If file doesn't exist, create an empty DataFrame
        df = pd.DataFrame(columns=columns)

    lst = []
    lst.append(df)
    # Append new data to the DataFrame
    new_data = pd.DataFrame([values], columns=columns)
    lst.append(new_data)
    df = pd.concat(lst, ignore_index=True)

    df.to_csv(filepath, index=False)
    print(df)

    return 