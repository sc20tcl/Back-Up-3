import pandas as pd
from scipy import stats

data = pd.read_csv('FilteredRequestsPerMinute.csv', parse_dates=['period'], index_col='period')

data['day_of_week'] = data.index.dayofweek

results_matrix_t = pd.DataFrame(index=range(7), columns=range(7))
results_matrix_p = pd.DataFrame(index=range(7), columns=range(7))

for i in range(7):
    for j in range(i+1, 7):  
        data_i = data[data['day_of_week'] == i]['count']
        data_j = data[data['day_of_week'] == j]['count']
        
        t_stat, p_value = stats.ttest_ind(data_i, data_j, equal_var=False, nan_policy='omit')
        
        results_matrix_t.loc[i, j] = t_stat
        results_matrix_p.loc[i, j] = p_value

print("T-statistic Matrix:")
print(results_matrix_t)
print("\nP-value Matrix:")
print(results_matrix_p)
