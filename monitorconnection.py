import os, platform, time
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt
import pandas as pd
from pingsettings import PingSettings
from emailer import send_email_report
from storageconfig import StorageConfig
from test_helper import do_not_run_in_test

class NetworkMonitor:
    def __init__(self, pingsettings = PingSettings()):
        self.host = pingsettings.pingHost
        self.count = pingsettings.pingCount
        self.sleeptime = pingsettings.pingInterval
        self.requiredSuccessfulPings = pingsettings.requiredSuccessfulPings
        
        self.initialize_storage()
    
    @do_not_run_in_test    
    def initialize_storage(self):
        self.check_storage_paths()
        self.move_log_file()
    
    #test-validated
    def check_storage_paths(self):
        for path in StorageConfig.storage_directories:
            if not os.path.exists(path):
                os.makedirs(path)
    
    #test-validated
    def move_log_file(self):
        current_date = self.get_current_date_string()
        new_log_path = f"{StorageConfig.log_storage_path}/{current_date}-log.txt"
        if os.path.exists(StorageConfig.log_file_name) and not os.path.exists(new_log_path):
            os.rename(StorageConfig.log_file_name, new_log_path)
    
    #test-validated
    def get_current_date_string(self):
        return datetime.now().strftime("%Y-%m-%d")

    def monitor_connection(self):
        while True:
            self.send_ping_and_log_results()

            if self.is_start_of_day():
                self.create_ping_latency_chart(StorageConfig.log_file_name)
                self.create_ping_success_chart(StorageConfig.log_file_name)
                send_email_report()
                self.flush_old_logs()

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
        
        with open(StorageConfig.log_file_name, "a") as file:
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

    def is_start_of_day(self):
        current_time = datetime.now()
        return \
            current_time <= datetime.now().replace(hour=0, minute=(self.sleeptime//60), second = 0) and \
            current_time >= datetime.now().replace(hour=0, minute=0, second = 0)
            
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
        plt.savefig(f'Plots/{plot_name}/{self.get_current_date_string()}-ping_{plot_name.lower()}_chart.png')
        
    def flush_old_logs(self):
        for directory in StorageConfig.storage_directories:
            self.delete_old_files_from_directory(directory)
    
    def delete_old_files_from_directory(self, path):
        storage_limit = datetime.now().date - timedelta(days=StorageConfig.days_of_history_to_keep)
        for file in os.listdir(path):
            if self.get_date_from_log_file(file) < storage_limit:
                os.remove(f"{path}/{file}")
    
    #test-validated
    def get_date_from_log_file(self, log_file):
        try:
            file_date = datetime.strptime(log_file[:10], "%Y-%m-%d").date()
            return file_date
        except:
            return datetime.now().date()