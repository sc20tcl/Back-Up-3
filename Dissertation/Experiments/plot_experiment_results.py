import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

original_data = pd.read_csv('../ScaledVD.csv', parse_dates=True, index_col='period')

def calculate_avg_http_req_95_duration(file_name):
    data = pd.read_csv(file_name)
    return data['http req duration (95%)'].mean()

def calculate_energy_consumption(file_name):
    data = pd.read_csv(file_name)
    minutes = len(data)
    hours = minutes / 60
    consumption = (16 * 270 * data['Node CPU Usage'] * hours) / 1000
    return consumption.sum()


def create_graph(start_date, end_date, graph_name, pod_count_file):
    start_datetime = pd.to_datetime(start_date)
    end_datetime = pd.to_datetime(end_date)

    original_filtered = original_data[start_date:end_date]
    pod_data = pd.read_csv(pod_count_file)
    pod_data.index = pd.date_range(start=start_datetime, periods=len(pod_data), freq='T')

    pod_filtered = pod_data[start_date:end_date]['Pod Count']


    fig, ax1 = plt.subplots(figsize=(10, 7))

    ax1.plot(original_filtered.index, original_filtered.values, label='Original QPS', linestyle='-', color='blue')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Queries Per Second (QPS)')
    ax1.tick_params(axis='y')

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=5)) 
    plt.xticks(rotation=45)

    ax2 = ax1.twinx()
    ax2.plot(pod_filtered.index, pod_filtered.values, label='Pod Count', linestyle='-', color='red')
    ax2.set_ylabel('Pod Count')
    ax2.tick_params(axis='y')
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

    time_format = '%H:%M'
    title = f"Comparison of Original and Predicted QPS between {start_datetime.strftime(time_format)} and {end_datetime.strftime(time_format)}"
    plt.title(title)
    fig.tight_layout()
    fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))

    plt.savefig(f'Experiment_plots/{graph_name}_predictive.png')
    plt.close(fig)  

highlight_ranges = [
    ('1998-06-24 10:24:00', '1998-06-24 11:24:00', "Lowest Variance", 'Experiment_Results/predictive_test1.csv'),
    ('1998-06-24 13:49:00', '1998-06-24 14:49:00', 'Largest Increase', 'Experiment_Results/predictive_test2.csv'),
    ('1998-06-24 16:02:00', '1998-06-24 17:02:00', 'Largest Decrease', 'Experiment_Results/predictive_test3.csv'),
    ('1998-06-24 20:11:00', '1998-06-24 21:11:00', "Highest Variance", 'Experiment_Results/predictive_test4.csv')
]

for start, end, name, file_name in highlight_ranges:
    create_graph(start, end, name, file_name)
    avg_http_95 = calculate_avg_http_req_95_duration(file_name)
    total_consumption = calculate_energy_consumption(file_name)
    print(f"Average HTTP 95% Duration for {name}: {avg_http_95:.2f} ms")
    print(f"Total Energy Consumption for {name}: {total_consumption:.2f} kWh")