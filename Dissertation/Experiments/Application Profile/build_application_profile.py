import pandas as pd

file_path = 'adjusted_data.csv'
data = pd.read_csv(file_path)

data['consumption'] = (16 * 270 * data['node response'] * 1) / 1000

def response_time_threshold(v_users):
    return 100 + (200 / 800) * v_users  

results = []

for v_users, group in data.groupby('virtual users'):
    threshold = response_time_threshold(v_users)
    filtered_group = group[group['http req duration (95%)'] < threshold]
    
    if not filtered_group.empty:

        top_replicas = filtered_group.nsmallest(3, 'consumption')
    else:
        top_replicas = group.nsmallest(3, 'http req duration (95%)')
    
    result_entry = {
        'queries per second rate': v_users,
        'replicas1': top_replicas.iloc[0]['replicas'] if len(top_replicas) > 0 else None,
        'replicas2': top_replicas.iloc[1]['replicas'] if len(top_replicas) > 1 else None,
        'replicas3': top_replicas.iloc[2]['replicas'] if len(top_replicas) > 2 else None
    }
    results.append(result_entry)

results_df = pd.DataFrame(results)

output_file_path = 'selected_replicas_top3.csv'
results_df.to_csv(output_file_path, index=False)

print(f"Results saved to {output_file_path}")
