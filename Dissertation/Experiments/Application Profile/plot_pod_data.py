import pandas as pd
import matplotlib.pyplot as plt

data_path = 'adjusted_data.csv'
data = pd.read_csv(data_path)

fig, ax = plt.subplots(figsize=(10, 6))
for replica in sorted(data['replicas'].unique()):
    subset = data[data['replicas'] == replica]
    ax.plot(subset['virtual users'], subset['node response'], linestyle='--', label=f'Replica Count of {replica}')

ax.set_title('CPU Utilisation against Queries Per Second by Replica Count')
ax.set_xlabel('Queries Per Second')
ax.set_ylabel('CPU Utilisation')
ax.legend(title='Replica Count')
plt.savefig('adjusted_flipped_node_utilisation.png')

fig, ax = plt.subplots(figsize=(10, 6))
for replica in sorted(data['replicas'].unique()):
    subset = data[data['replicas'] == replica]
    ax.plot(subset['virtual users'], subset['http req duration (95%)'], linestyle='--', label=f'Replica Count of  {replica}')

ax.set_title('HTTP Request Duration (95%) against Queries Per Second by Replica Count')
ax.set_xlabel('Queries Per Second')
ax.set_ylabel('HTTP Request Duration (95%)')
ax.legend(title='Replica Count')
plt.savefig('flipped_http_duration.png')