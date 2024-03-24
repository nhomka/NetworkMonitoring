import os
import platform
import time
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pingsettings import pingsettings

def ping(host):
    ping_str = build_ping_string(host)

    # Ping
    response = os.system(ping_str)
    success = successful_ping(response)
    latency = 0
    if success:
        latency = get_ping_latency(ping_str)

    return success, latency

def build_ping_string(host):
    return f"ping {get_os_specific_ping_str()} {host}"

def get_os_specific_ping_str():
    return "-n 1" if platform.system().lower() == "windows" else "-c 1"

def successful_ping(response):
    return response == 0

def get_ping_latency(ping_str):
    if platform.system().lower() == "windows":
        output = os.popen(ping_str).read()
        latency = float(output.split("Average = ")[1].split("ms")[0])
    else:
        output = os.popen(ping_str).read()
        latency = float(output.split("time=")[1].split(" ")[0])
    return latency

def monitor_connection(pingsettings):
    host = pingsettings.pingHost
    count = pingsettings.pingCount
    sleeptime = pingsettings.pingInterval
    requiredSuccessfulPings = pingsettings.requiredSuccessfulPings
    
    while True:
        success_count = 0
        for _ in range(count):
            result, latency = ping(host)
            if result:
                success_count += 1
            time.sleep(1)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Success" if success_count >= requiredSuccessfulPings else "Failure"
        
        with open("log.txt", "a") as file:
            file.write(f"{timestamp} - {status} - {latency}\n")

        if generate_start_of_day_plots(sleeptime):
            create_ping_latency_chart("log.txt")
            create_ping_success_chart("log.txt")

        time.sleep(sleeptime-count)  # Wait for the remaining time in the interval

def generate_start_of_day_plots(sleeptime):
    current_time = datetime.now()
    return \
        current_time <= datetime.now().replace(hour=0, minute=(sleeptime//60), second = 0) and \
        current_time >= datetime.now().replace(hour=0, minute=0, second = 0)
        
def create_ping_latency_chart(log_file):
    df = create_dataframe_from_log(log_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    plot_chart('Latency', df)
    
def create_ping_success_chart(log_file):
    df = create_dataframe_from_log(log_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['success'] = df['status'].apply(lambda x: 1 if x == 'Success' else 0)
    plot_chart('Success', df)
    
def create_dataframe_from_log(log_file):
    return pd.read_csv(log_file, sep=" - ", names=["timestamp", "status", "latency"])
    
def plot_chart(plot_name, dataframe):
    dataframe.plot(x='timestamp', y=plot_name.lower())
    plt.title(f'Ping {plot_name} Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel(plot_name)
    plt.savefig(f'Plots/{plot_name}/ping_{plot_name.lower()}_chart.png')

settings = pingsettings()
settings.pingCount = 5
settings.pingInterval = 60
settings.pingHost = "google.com"

monitor_connection(settings)