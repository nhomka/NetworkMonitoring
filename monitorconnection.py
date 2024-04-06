import os, platform, time
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pingsettings import PingSettings
from emailer import send_email_report
from file_storage_configuration import log_file_name, clean_old_logs, plots_storage_path
from datetime_functions import current_date_string, is_start_of_day
from pinger import get_pinger_class

class NetworkMonitor:
    def __init__(self, pingsettings = PingSettings()):
        self.settings = pingsettings
        self.pinger = get_pinger_class(self.settings)

    def monitor_connection(self):
        while True:
            success, latency = self.pinger.ping()
            self.log_results(success, latency)

            if is_start_of_day(self.settings.interval):
                self.create_ping_latency_chart(log_file_name)
                self.create_ping_success_chart(log_file_name)
                send_email_report()
                clean_old_logs()

            time.sleep(self.settings.interval)  # Wait for the remaining time in the interval

    def log_results(self, success, latency):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file_name, "a") as file:
            file.write(f"{timestamp},{success},{latency}\n")
            
    def create_ping_latency_chart(self, log_file):
        df = self.create_dataframe_from_log(log_file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        self.plot_chart('Latency', df)
        
    def create_ping_success_chart(self, log_file):
        df = self.create_dataframe_from_log(log_file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['success'] = df['status'].apply(lambda x: 1 if x == 'Success' else 0)
        self.plot_chart('Success', df)
        
    def create_dataframe_from_log(self, log_file):
        return pd.read_csv(log_file, sep=",", names=["timestamp", "status", "latency"])
        
    def plot_chart(self, plot_name, dataframe):
        dataframe.plot(x='timestamp', y=plot_name.lower())
        plt.title(f'Ping {plot_name} Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel(plot_name)
        plt.savefig(f'{plots_storage_path}/{plot_name}/{current_date_string()}-ping_{plot_name.lower()}_chart.png')
    
