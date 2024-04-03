import os
from test_helper import do_not_run_in_test
from datetime_functions import current_date_string, date_to_remove_old_files

days_of_history_to_keep = 28
days_of_history_per_file = 1

base_storage_path = os.environ["ProgramFiles"] if os.name == "nt" else os.environ["HOME"]
app_storage_path = f"{base_storage_path}/NetworkMonitor"

latency_storage_path = app_storage_path + "/Plots/Latency"
success_storage_path = app_storage_path + "/Plots/Success"
log_storage_path = app_storage_path + "/Logs"
log_file_name = app_storage_path + "/Logs/log.txt"
storage_directories = [latency_storage_path, success_storage_path, log_storage_path]

@do_not_run_in_test    
def initialize_storage(self):
    self.check_storage_paths()
    self.move_log_file()

#test-validated
def check_storage_paths():
        for path in storage_directories:
            if not os.path.exists(path):
                os.makedirs(path)
                
#test-validated
def move_log_file():
    current_date = current_date_string()
    new_log_path = f"{log_storage_path}/{current_date}-log.txt"
    if os.path.exists(log_file_name) and not os.path.exists(new_log_path):
        os.rename(log_file_name, new_log_path)
        
def clean_old_logs(self):
        for directory in storage_directories:
            self.delete_old_files_from_directory(directory)

def delete_old_files_from_directory(self, path):
    storage_limit = date_to_remove_old_files(days_of_history_to_keep)
    for file in os.listdir(path):
        if self.get_date_from_log_file(file) < storage_limit:
            os.remove(f"{path}/{file}")