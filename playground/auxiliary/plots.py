import pandas as pd
import matplotlib.pyplot as plt
import textwrap

def plot_graphs_from_csv(file_path):
    # Read the CSV file into a pandas DataFrame
    data = pd.read_csv(file_path)
    
    # Extract the System_specs column for labeling
    system_specs = data['System_specs']
    
    # Iterate over each column (excluding the System_specs column) and plot the graphs
    for column in data.columns[1:]:
        plt.figure(figsize=(14, 8))  # Increase figure size
        plt.bar(range(len(system_specs)), data[column], align='center')
        # plt.xlabel('System Specs')
        # plt.ylabel(column)
        plt.title(f'{column}')

        # Wrap the labels to fit better
        wrapped_labels = ['\n'.join(textwrap.wrap(label, 20)) for label in system_specs]
        plt.xticks(range(len(system_specs)), wrapped_labels, rotation=45, ha='right', fontsize=10)

        # Ensure all bars and labels are shown
        plt.subplots_adjust(bottom=0.25, right=0.95, top=0.90)  # Adjust layout to make room for the labels

        plt.tight_layout()  # Adjust layout to make room for the labels
        plt.show()


path = '/Users/aris/Documents/GitHub/CloudSimPy/playground/DAG/extracted_data/data.csv'
# Call the function with the CSV data
plot_graphs_from_csv(path)
