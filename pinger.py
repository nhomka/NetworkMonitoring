from datetime import datetime
import time, platform, os
from file_storage_configuration import log_file_name
from pingsettings import PingSettings

settings = PingSettings()

def send_ping_and_log_results():
    result, latency = ping()
    time.sleep(1)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Success" if result else "Failure"
    
    with open(log_file_name, "a") as file:
        file.write(f"{timestamp},{status},{latency}\n")

def ping():
    ping_command = build_ping_command()
    success, latency = send_ping_command(ping_command)
    return success, latency

#test-validated
def build_ping_command():
    return f"ping {get_os_specific_ping()} {settings.host}"

#test-validated
def get_os_specific_ping():
    return "-n 1" if platform.system().lower() == "windows" else "-c 1"

def send_ping_command(ping_command):
    success = is_ping_successful(ping_command)
    latency = get_ping_latency(ping_command) if success else 0
    return success, latency

def is_ping_successful(ping_command):
    response = os.system(ping_command)
    return response == 0

def get_ping_latency(ping_str):
    if platform.system().lower() == "windows":
        output = os.popen(ping_str).read()
        latency = float(output.split("Average = ")[1].split("ms")[0])
    else:
        output = os.popen(ping_str).read()
        latency = float(output.split("time=")[1].split(" ")[0])
    return latency