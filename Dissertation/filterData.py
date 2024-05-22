import pandas as pd

file_path = 'RequstsPerMinute.csv'

data = pd.read_csv(file_path)

data['period'] = pd.to_datetime(data['period'])

start_date = '1998-06-09 00:00:00'
end_date = '1998-06-29 00:00:00'
filtered_data = data[(data['period'] >= start_date) & (data['period'] <= end_date)]

filtered_data.to_csv('FilteredRequestsPerMinute.csv', index=False)

test_start_date = '1998-06-15 00:00:00'
test_end_date = '1998-06-20 23:59:59'
test_data = data[(data['period'] >= test_start_date) & (data['period'] <= test_end_date)]
test_data.to_csv('TestData.csv', index=False)

validate_start_date = '1998-06-24 00:00:00'
validate_end_date = '1998-06-24 23:59:59'
test_data = data[(data['period'] >= validate_start_date) & (data['period'] <= validate_end_date)]
test_data.to_csv('ValidateData.csv', index=False)

print("Filtered and test data saved successfully.")
