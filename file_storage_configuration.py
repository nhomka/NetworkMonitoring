import os
from helper_functions import do_not_run_in_test
from datetime_functions import current_date_string, date_to_remove_old_files, get_date_from_log_file
from configuration import FileSystemInfo as fs

@do_not_run_in_test    
def initialize_storage() -> None:
    check_storage_paths()
    move_log_file()

# test-validated
def check_storage_paths() -> None:
        for path in fs.STORAGE_DIRECTORIES:
            if not os.path.exists(path):
                os.makedirs(path)
                
# test-validated
def move_log_file() -> None:
    current_date = current_date_string()
    new_log_path = f"{fs.LOG_STORAGE_PATH}/{current_date}-log.txt"
    if os.path.exists(fs.LOG_FILE_NAME) and not os.path.exists(new_log_path):
        os.rename(fs.LOG_FILE_NAME, new_log_path)

def clean_old_logs() -> None:
        for directory in fs.STORAGE_DIRECTORIES:
            delete_old_files_from_directory(directory)

# test-validated
def delete_old_files_from_directory(path: str) -> None:
    storage_limit = date_to_remove_old_files(fs.DAYS_OF_HISTORY)
    for file in os.listdir(path):
        if get_date_from_log_file(file) < storage_limit:
            os.removedirs(f"{path}/{file}")