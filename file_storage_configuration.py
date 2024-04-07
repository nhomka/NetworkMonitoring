import os
from test_helper import do_not_run_in_test
from datetime_functions import current_date_string, date_to_remove_old_files, get_date_from_log_file
from file_paths import *

@do_not_run_in_test    
def initialize_storage() -> None:
    check_storage_paths()
    move_log_file()

# test-validated
def check_storage_paths() -> None:
        for path in storage_directories:
            if not os.path.exists(path):
                os.makedirs(path)
                
# test-validated
def move_log_file() -> None:
    current_date = current_date_string()
    new_log_path = f"{log_storage_path}/{current_date}-log.txt"
    if os.path.exists(log_file_name) and not os.path.exists(new_log_path):
        os.rename(log_file_name, new_log_path)

def clean_old_logs() -> None:
        for directory in storage_directories:
            delete_old_files_from_directory(directory)

# test-validated
def delete_old_files_from_directory(path: str) -> None:
    storage_limit = date_to_remove_old_files(days_of_history_to_keep)
    for file in os.listdir(path):
        if get_date_from_log_file(file) < storage_limit:
            os.removedirs(f"{path}/{file}")