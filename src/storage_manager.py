import os
from src.helper_functions import do_not_run_in_test
from src.datetime_util import current_date_string, date_to_remove_old_files, get_date_from_log_file
from config.file_config import FileSystemInfo

class StorageManager:
    def __init__(self, fs: FileSystemInfo):
        self.fs = fs
        self._initialize_storage()

    @do_not_run_in_test   
    def _initialize_storage(self) -> None:
        self._check_storage_paths()
        self.clean_old_logs()
        
    def _check_storage_paths(self) -> None:
        for path in self.fs.STORAGE_DIRECTORIES:
            if not os.path.exists(path):
                os.makedirs(path)
    
    def clean_old_logs(self) -> None:
        self._archive_latest_log_file()
        for directory in self.fs.STORAGE_DIRECTORIES:
            self._delete_old_files_from_directory(directory)

    def _archive_latest_log_file(self) -> None:
        current_date = current_date_string()
        new_log_path = f"{self.fs.LOG_STORAGE_PATH}/{current_date}-log.txt"
        if os.path.exists(self.fs.LOG_FILE_NAME) and not os.path.exists(new_log_path):
            os.rename(self.fs.LOG_FILE_NAME, new_log_path)

    def _delete_old_files_from_directory(self, path: str) -> None:
        storage_limit = date_to_remove_old_files(self.fs.DAYS_OF_HISTORY)
        for file in os.listdir(path):
            if get_date_from_log_file(file) < storage_limit:
                os.removedirs(f"{path}/{file}")