import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import KFold

def plot_daily():
    daily_patterns = data.groupby('minute_of_day')['count'].mean()
    plt.figure(figsize=(12, 6))
    daily_patterns.plot(title='Average RPM per Minute of Day')
    plt.xlabel('Minute of Day')
    plt.ylabel('Average RPM')
    plt.tight_layout()
    plt.savefig('FilteredDSG/daily_patterns_final.png')

def plot_weekly(): 
    data['minute_of_week'] = (data.index.dayofweek * 24 * 60) + (data.index.hour * 60) + data.index.minute

    minute_weekly_patterns = data.groupby('minute_of_week')['count'].mean()

    plt.figure(figsize=(15, 6))
    minute_weekly_patterns.plot(title='Average RPM per Hour of Week')
    plt.xlabel('Hour of Week')
    plt.ylabel('Average RPM')

    tick_positions = np.arange(0, 60*24*7, 60*24)  
    tick_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    plt.xticks(tick_positions, tick_labels, rotation=45)

    plt.grid(True)
    plt.tight_layout()
    plt.savefig('FilteredDSG/weekly_patterns_final.png')

def plot_monthly():
    june_data = data[data.index.month == 6]
    july_data = data[data.index.month == 7]

    fig, axs = plt.subplots(2, 1, figsize=(12, 12))

    axs[0].plot(june_data.index, june_data['count'], label='June Data Points')
    axs[0].set_title('Data Points in June')
    axs[0].set_xlabel('Date')
    axs[0].set_ylabel('RPM')
    axs[0].legend()

    axs[1].plot(july_data.index, july_data['count'], label='July Data Points', color='orange')
    axs[1].set_title('Data Points in July')
    axs[1].set_xlabel('Date')
    axs[1].set_ylabel('RPM')
    axs[1].legend()

    plt.tight_layout()
    plt.savefig('FilteredDSG/june_july_data_points.png')

def plot_full_set():
    plt.figure(figsize=(12, 6))
    data['count'].plot(title='RPM Over Entire Dataset')
    plt.xlabel('Date')
    plt.ylabel('RPM')
    plt.tight_layout()
    plt.savefig('FilteredDSG/entire_dataset_trend_final.png')

data = pd.read_csv('FilteredRequestsPerMinute.csv', parse_dates=['period'], index_col='period')

data['minute_of_day'] = data.index.hour * 60 + data.index.minute 
data['day_of_week'] = data.index.dayofweek 

plot_daily()
plot_weekly()
plot_monthly()
plot_full_set()
