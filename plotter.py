import matplotlib.pyplot as plt
import pandas as pd
from datetime_helper import current_date_string
from config.file_config import FileSystemInfo as fs

def build_charts() -> None:
    _build_latency_chart()
    _build_connection_chart()
    
def _build_latency_chart() -> None:
    df = _build_dataframe_from_log()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    _save_plot('Latency', df)
    
def _build_connection_chart() -> None:
    df = _build_dataframe_from_log()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['success'] = df['status'].apply(lambda x: 1 if x == 'Success' else 0)
    _save_plot('Success', df)
    
def _build_dataframe_from_log() -> pd.DataFrame:
    return pd.read_csv(fs.LOG_FILE_NAME, sep=",", names=["timestamp", "status", "latency"])
    
def _save_plot(plot_name: str, dataframe: pd.DataFrame) -> None:
    dataframe.plot(x='timestamp', y=plot_name.lower())
    plt.title(f'Ping {plot_name} Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel(plot_name)
    plt.savefig(f'{fs.PLOTS_STORAGE_PATH}/{plot_name}/{current_date_string()}-ping_{plot_name.lower()}_chart.png')