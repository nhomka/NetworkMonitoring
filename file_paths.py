import os

days_of_history_to_keep = 28
days_of_history_per_file = 1

base_storage_path = os.environ["HOMEPATH"] if os.name == "nt" else os.environ["HOME"]
app_storage_path = f"{base_storage_path}\\NetworkMonitor"

plots_storage_path = app_storage_path + "\\Plots"
latency_storage_path = app_storage_path + "\\Plots\\Latency"
success_storage_path = app_storage_path + "\\Plots\\Success"
log_storage_path = app_storage_path + "\\Logs"
log_file_name = app_storage_path + "\\Logs\\log.txt"

storage_directories = [latency_storage_path, success_storage_path, log_storage_path]