import os
import platform
import time
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd




def ping(host):
    # Ping parameters as function of OS
    ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"

    # Ping
    response = os.system("ping " + ping_str + " " + host)
    success = response == 0
    latency = None
    if success:
        # Extract latency from ping response
        if platform.system().lower() == "windows":
            output = os.popen(f"ping {ping_str} {host}").read()
            latency = float(output.split("Average = ")[1].split("ms")[0])
        else:
            output = os.popen(f"ping {ping_str} {host}").read()
            latency = float(output.split("time=")[1].split(" ")[0])

    return success, latency

def monitor_connection(host, sleep_time):
    while True:
        seconds_lapsed = 0
        success_count = 0
        for _ in range(5):
            result, latency = ping(host)
            if result:
                success_count += 1
                break
            time.sleep(1)  # Wait for 1 second between pings
            seconds_lapsed += 1

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Success" if success_count >= 1 else "Failure"
        

        with open("log.txt", "a") as file:
            file.write(f"{timestamp} - {status} - {latency}\n")

        current_time = datetime.now()
        if current_time <= datetime.now().replace(hour=0, minute=1, second=sleep_time%60) \
        and current_time >= datetime.now().replace(hour=0, minute=0, second=sleep_time%60):
            create_ping_latency_chart("log.txt")
            create_ping_success_chart("log.txt")

        time.sleep(sleep_time-seconds_lapsed)  # Wait for 30 seconds before pinging again

def create_ping_latency_chart(log_file):
    df = pd.read_csv(log_file, sep=" - ", names=["timestamp", "status", "latency"])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.plot(x='timestamp', y='latency')
    plt.title('Ping Latency Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Latency')
    plt.savefig('Plots/Latency/ping_latency_chart.png')
    
def create_ping_success_chart(log_file):
    df = pd.read_csv(log_file, sep=" - ", names=["timestamp", "status", "latency"])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['success'] = df['status'].apply(lambda x: 1 if x == 'Success' else 0)
    df.plot(x='timestamp', y='success')
    plt.title('Ping Success Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Success')
    plt.savefig('Plots/Success/ping_success_chart.png')

monitor_connection("google.com", 60)