import os, platform, time
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pingsettings import PingSettings
from emailer import send_email_report
from file_storage_configuration import initialize_storage, log_file_name, clean_old_logs
from datetime_functions import current_date_string, is_start_of_day

class NetworkMonitor:
    def __init__(self, pingsettings = PingSettings()):
        self.host = pingsettings.pingHost
        self.count = pingsettings.pingCount
        self.sleeptime = pingsettings.pingInterval
        self.requiredSuccessfulPings = pingsettings.requiredSuccessfulPings
        
        initialize_storage()

    def monitor_connection(self):
        while True:
            self.send_ping_and_log_results()

            if is_start_of_day(self.sleeptime):
                self.create_ping_latency_chart(log_file_name)
                self.create_ping_success_chart(log_file_name)
                send_email_report()
                clean_old_logs()

            time.sleep(self.sleeptime-self.count)  # Wait for the remaining time in the interval

    def send_ping_and_log_results(self):
        success_count = 0
        for _ in range(self.count):
            result, latency = self.ping()
            if result:
                success_count += 1
            time.sleep(1)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Success" if success_count >= self.requiredSuccessfulPings else "Failure"
        
        with open(log_file_name, "a") as file:
            file.write(f"{timestamp},{status},{latency}\n")

    def ping(self):
        ping_command = self.build_ping_command()
        success, latency = self.send_ping_command(ping_command)
        return success, latency

    #test-validated
    def build_ping_command(self):
        return f"ping {self.get_os_specific_ping()} {self.host}"

    #test-validated
    def get_os_specific_ping(self):
        return "-n 1" if platform.system().lower() == "windows" else "-c 1"

    def send_ping_command(self, ping_command):
        success = self.is_ping_successful(ping_command)
        latency = self.get_ping_latency(ping_command) if success else 0
        return success, latency

    def is_ping_successful(self, ping_command):
        response = os.system(ping_command)
        return response == 0

    def get_ping_latency(self, ping_str):
        if platform.system().lower() == "windows":
            output = os.popen(ping_str).read()
            latency = float(output.split("Average = ")[1].split("ms")[0])
        else:
            output = os.popen(ping_str).read()
            latency = float(output.split("time=")[1].split(" ")[0])
        return latency
            
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
        plt.savefig(f'Plots/{plot_name}/{current_date_string()}-ping_{plot_name.lower()}_chart.png')
    
