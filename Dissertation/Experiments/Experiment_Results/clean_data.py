import pandas as pd

def convert_to_ms(value):
    if pd.isna(value):
        return value  # Return NaN as it is
    if isinstance(value, str):  # Check if the value is string to avoid TypeError
        if "ms" in value:
            return float(value.replace("ms", ""))
        elif "s" in value:
            return float(value.replace("s", "")) * 1000
    return value

def process_csv(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Apply the conversion function to the relevant columns
    data["http req duration (90%)"] = data["http req duration (90%)"].apply(convert_to_ms)
    data["http req duration (95%)"] = data["http req duration (95%)"].apply(convert_to_ms)

    # Save the modified data to the same CSV file
    data.to_csv(file_path, index=False)

# Example usage:
file_path = 'predictive_test4.csv'  # Update with your CSV file path
process_csv(file_path)