import os
import platform
import time
from datetime import datetime



def ping(host):
    # Ping parameters as function of OS
    ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"

    # Ping
    return os.system("ping " + ping_str + " " + host) == 0

def monitor_connection(host, sleep_time):
    while True:
        seconds_lapsed = 0
        success_count = 0
        for _ in range(5):
            result = ping(host)
            if result:
                success_count += 1
                break
            time.sleep(1)  # Wait for 1 second between pings
            seconds_lapsed += 1

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Success" if success_count >= 1 else "Failure"

        with open("log.txt", "a") as file:
            file.write(f"{timestamp} - {status}\n")

        time.sleep(sleep_time-seconds_lapsed)  # Wait for 30 seconds before pinging again

monitor_connection("google.com", 60)