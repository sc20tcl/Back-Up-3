import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv('RequstsPerMinute.csv', parse_dates=['period'], index_col='period')

def plot_traffic(data, start_date, end_date, highlight_ranges):
    filtered_data = data.loc[start_date:end_date]

    fig, ax = plt.subplots(figsize=(10, 5))
    
    ax.plot(filtered_data.index, filtered_data['count'], label='Traffic count', color='black')

    for range_start, range_end, color, label in highlight_ranges:
        
        range_data = data.loc[range_start:range_end]
        ax.plot(range_data.index, range_data['count'], label=label, linewidth=2, color=color)

    ax.set_title('Traffic Count Over Time')
    ax.set_xlabel('Time')
    ax.set_ylabel('Traffic Count')

    # ax.xaxis.set_major_locator(mdates.HourLocator())  
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) 

    ax.xaxis.set_major_locator(mdates.DayLocator())  # Set locator for each day
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))  # Set formatter to day:monthr

    plt.xticks(rotation=45)
    

    ax.legend()
    plt.tight_layout()
    plt.savefig('FilteredDSG/TrainTestSplit.png')
    plt.show()

# Train test validate split
# start_date = '1998-06-14 00:00:00'
# end_date = '1998-06-26 23:59:00'
# highlight_ranges = [
#     ('1998-06-15 00:00:00', '1998-06-18 23:59:00', 'green', "Training Data"),  
#     ('1998-06-19 00:00:00', '1998-06-19 23:59:00', 'red', "Testing Data"),
#     ('1998-06-24 00:00:00', '1998-06-24 23:59:00', 'orange', "Evaluation Data")
# ]
    
start_date = '1998-06-24 00:00:00'
end_date = '1998-06-24 23:59:00'
highlight_ranges = [
    ('1998-06-24 16:02:00', '1998-06-24 17:02:00', 'red', 'Largest Decrease'), # highest decrease
    ('1998-06-24 13:49:00', '1998-06-24 14:49:00', 'blue', 'Largest Increase'), # highest increase
    ('1998-06-24 10:24:00', '1998-06-24 11:24:00', 'green', "Lowest Variance"), # lowest variance
    ('1998-06-24 20:01:00', '1998-06-24 21:01:00', 'orange', "Highest Variance") # highest variance

]

plot_traffic(df, start_date, end_date, highlight_ranges)