import pandas as pd
import matplotlib.pyplot as plt
import textwrap
import argparse

def plot_graphs_from_csv(file_path):
    # Read the CSV file into a pandas DataFrame
    data = pd.read_csv(file_path)
    
    # Extract the System_specs column for labeling
    system_specs = data['Number of episodes']
    
    # Define colors for each position
    colors = ['green', 'red', 'blue']
    
    # Iterate over each column (excluding the System_specs column) and plot the graphs
    for column in data.columns[1:]:
        plt.figure(figsize=(14, 8))  # Increase figure size
        bars = plt.bar(range(len(system_specs)), data[column], align='center')

        # Set colors for bars based on their position
        for i, bar in enumerate(bars):
            # if i == 0 or i == 1:
            #     bar.set_color('grey')
            bar.set_color(colors[(i) % 3])
        
        plt.title(f'{column}')

        # Wrap the labels to fit better
        wrapped_labels = [label for label in system_specs]
        plt.xticks(range(len(system_specs)), wrapped_labels, rotation=0, fontsize=10)

        # Ensure all bars and labels are shown
        plt.subplots_adjust(bottom=0.25, right=0.95, top=0.90)  # Adjust layout to make room for the labels

        # Add legend
        handles = [plt.Rectangle((0,0),1,1, color=color) for color in colors]
        labels = ['200 sec response time threshold', '300 sec response time threshold', '400 sec response time threshold']
        plt.legend(handles, labels)

        plt.tight_layout()  # Adjust layout to make room for the labels
        plt.show()

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Plot graphs from a CSV file.')
    
    # Add the file path argument
    parser.add_argument('file_path', type=str, help='Path to the CSV file.')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Call the function with the provided file path
    plot_graphs_from_csv(args.file_path)

if __name__ == '__main__':
    main()
