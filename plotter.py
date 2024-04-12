import matplotlib.pyplot as plt
import pandas as pd
from datetime_helper import current_date_string
from config.file_config import FileSystemInfo

def build_charts(fs: FileSystemInfo) -> None:
    dfs = _build_dataframes_from_log(fs)
    for df in dfs.values():
        _build_latency_chart(df, fs)
        _build_connection_chart(df, fs)
    
def _build_latency_chart(df: pd.DataFrame, fs: FileSystemInfo) -> None:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    _save_plot('Latency', df, fs)
    
def _build_connection_chart(df: pd.DataFrame, fs: FileSystemInfo) -> None:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['success'] = df['status'].apply(lambda x: 1 if x == 'Success' else 0)
    _save_plot('Success', df, fs)
    
def _build_dataframe_from_log(fs: FileSystemInfo) -> pd.DataFrame:
    return pd.read_csv(fs.LOG_FILE_NAME, sep=",", names=["friendly_name","timestamp", "status", "latency"])

def _build_dataframes_from_log(fs: FileSystemInfo) -> dict[str, pd.DataFrame]:
    df = _build_dataframe_from_log(fs)
    dfs = {}
    for friendly_name in df['friendly_name'].unique():
        dfs[friendly_name] = df[df['friendly_name'] == friendly_name]
    return dfs
    
def _save_plot(plot_name: str, dataframe: pd.DataFrame, fs: FileSystemInfo) -> None:
    dataframe.plot(x='timestamp', y=plot_name.lower())
    plt.title(f'Ping {plot_name} Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel(plot_name)
    plt.savefig(f'{fs.PLOTS_STORAGE_PATH}/{plot_name}/{current_date_string()}-ping_{plot_name.lower()}_chart.png')