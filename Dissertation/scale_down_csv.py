import pandas as pd

def scale_data(input_file, output_file):
    # Load the data from the CSV file
    data = pd.read_csv(input_file)
    
    # Scale the 'count' column by dividing by 3
    data['count'] = (data['count'] / 3).astype(int)
    
    # Save the scaled data to a new CSV file
    data.to_csv(output_file, index=False)
    print(f"Data scaled and saved to {output_file}")

# Specify the name of your input file and output file
input_filename = 'ValidateData.csv'
output_filename = 'SacledVD.csv'

# Call the function with the file names
scale_data(input_filename, output_filename)