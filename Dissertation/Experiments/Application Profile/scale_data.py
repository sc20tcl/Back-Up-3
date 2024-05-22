import pandas as pd

# Load the dataset
data_path = 'adjusted_data.csv'  # Replace 'path_to_your_dataset.csv' with the actual path to your dataset
data = pd.read_csv(data_path)

# Adjust the node response data
data['node response'] = data.apply(lambda row: row['node response'] * (1 + 0.01 * (row['replicas'] - 5)), axis=1)

# Save the adjusted dataset to a new CSV file
adjusted_data_path = 'adjusted_data.csv'
data.to_csv(adjusted_data_path, index=False)
