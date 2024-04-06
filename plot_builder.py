import matplotlib.pyplot as plt
import pandas as pd
from datetime_functions import current_date_string
from file_paths import plots_storage_path, log_file_name

def build_charts():
    _build_latency_chart()
    _build_connection_chart()
    
def _build_latency_chart():
    df = _build_dataframe_from_log()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    _save_plot('Latency', df)
    
def _build_connection_chart():
    df = _build_dataframe_from_log()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['success'] = df['status'].apply(lambda x: 1 if x == 'Success' else 0)
    _save_plot('Success', df)
    
def _build_dataframe_from_log():
    return pd.read_csv(log_file_name, sep=",", names=["timestamp", "status", "latency"])
    
def _save_plot(plot_name, dataframe):
    dataframe.plot(x='timestamp', y=plot_name.lower())
    plt.title(f'Ping {plot_name} Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel(plot_name)
    plt.savefig(f'{plots_storage_path}/{plot_name}/{current_date_string()}-ping_{plot_name.lower()}_chart.png')