import pandas as pd

data = pd.read_csv('ValidateData.csv', parse_dates=['period'])

data['rolling_diff'] = data['count'].diff() 
data['rolling_hourly_diff'] = data['rolling_diff'].rolling(window=60).sum()  

data = data.dropna(subset=['rolling_hourly_diff'])

max_increase = data['rolling_hourly_diff'].max()
print(data['rolling_hourly_diff'])
min_decrease = data['rolling_hourly_diff'].min()

max_increase_time = data[data['rolling_hourly_diff'] == max_increase]['period'].iloc[0]
min_decrease_time = data[data['rolling_hourly_diff'] == min_decrease]['period'].iloc[0]

data['rolling_hourly_variance'] = data['count'].rolling(window=60).var()

max_variance = data['rolling_hourly_variance'].max()
min_variance = data['rolling_hourly_variance'].min()

max_variance_time = data[data['rolling_hourly_variance'] == max_variance]['period'].iloc[0]
min_variance_time = data[data['rolling_hourly_variance'] == min_variance]['period'].iloc[0]

print(f"Maximum Increase (Rolling): {max_increase} at {max_increase_time}")
print(f"Minimum Decrease (Rolling): {min_decrease} at {min_decrease_time}")
print(f"Maximum Variance (Rolling): {max_variance} at {max_variance_time}")
print(f"Minimum Variance (Rolling): {min_variance} at {min_variance_time}")