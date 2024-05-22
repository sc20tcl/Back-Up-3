import pandas as pd

def convert_to_ms(value):
    if pd.isna(value):
        return value 
    if isinstance(value, str):  
        if "ms" in value:
            return float(value.replace("ms", ""))
        elif "s" in value:
            return float(value.replace("s", "")) * 1000
    return value

def process_csv(file_path):

    data = pd.read_csv(file_path)

    
    data["http req duration (90%)"] = data["http req duration (90%)"].apply(convert_to_ms)
    data["http req duration (95%)"] = data["http req duration (95%)"].apply(convert_to_ms)


    data.to_csv(file_path, index=False)

def clean_csv(file_path):

    data = pd.read_csv(file_path)

    data.drop(columns=["pod response", "http req duration (90%)"], inplace=True)
    data.to_csv(file_path, index=False)




file_path = 'scenario_pod_model.csv' 
process_csv(file_path)
clean_csv(file_path)