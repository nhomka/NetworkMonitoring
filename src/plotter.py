import matplotlib.pyplot as plt
import pandas as pd
from datetime_util import current_date_string
from config.file_config import FileSystemInfo

class Plotter:
    
    def __init__(self, fs: FileSystemInfo):
        self.fs = fs

    def build_charts(self) -> None:
        dfs = self._build_dataframes_from_log()
        for df in dfs.values():
            self._build_latency_chart(df)
            self._build_connection_chart(df)
        
    def _build_latency_chart(self, df: pd.DataFrame) -> None:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        self._save_plot('Latency', df)
        
    def _build_connection_chart(self, df: pd.DataFrame) -> None:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['success'] = df['status'].apply(lambda x: 1 if x == 'True' else 0)
        self._save_plot('Success', df)
        
    def _build_dataframe_from_log(self) -> pd.DataFrame:
        return pd.read_csv(self.fs.LOG_FILE_NAME, sep=",", names=["friendly_name","timestamp", "status", "latency"])

    def _build_dataframes_from_log(self) -> dict[str, pd.DataFrame]:
        df = self._build_dataframe_from_log()
        dfs = {}
        for friendly_name in df['friendly_name'].unique():
            dfs[friendly_name] = df[df['friendly_name'] == friendly_name]
        return dfs
        
    def _save_plot(self, plot_name: str, dataframe: pd.DataFrame) -> None:
        dataframe.plot(x='timestamp', y=plot_name.lower())
        plt.title(f'Ping {plot_name} Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel(plot_name)
        plt.savefig(f'{self.fs.PLOTS_STORAGE_PATH}/{plot_name}/{current_date_string()}-ping_{plot_name.lower()}_chart.png')