class StorageConfig:
    days_of_history_to_keep = 28
    days_of_history_per_file = 1
    
    latency_storage_path = "./Plots/Latency"
    success_storage_path = "./Plots/Success"
    log_storage_path = "./Logs"
    log_file_name = "log.txt"
    storage_directories = [latency_storage_path, success_storage_path, log_storage_path]