import datetime
from freezegun import freeze_time
from config.file_config import FileSystemInfo
from src.storage_manager import StorageManager
import os

file_system_info = FileSystemInfo()
storage_manager = StorageManager(file_system_info)

storage_directories = file_system_info.STORAGE_DIRECTORIES
log_storage_path = file_system_info.LOG_STORAGE_PATH
log_file_name = file_system_info.LOG_FILE_NAME
days_of_history = file_system_info.DAYS_OF_HISTORY

def test_on_creation_check_storage_directories(fs):
    for path in storage_directories:
        assert os.path.exists(path) == False
    storage_manager._check_storage_paths()
    for path in storage_directories:
        assert os.path.exists(path) == True 

@freeze_time("2024-03-25")
def test_delete_old_files_from_directory(fs):
    excess_days = 10
    directory = log_storage_path
    os.makedirs(directory)
    
    for i in range(0, days_of_history + excess_days):
        date = datetime.datetime.now().date() - datetime.timedelta(days=i)
        formatted_date = date.strftime("%Y-%m-%d")
        file_name = f"{directory}/{formatted_date}-log.txt"
        os.makedirs(file_name)
    
    # check that all files have been created
    assert len(os.listdir(directory)) == days_of_history + excess_days
    storage_manager._delete_old_files_from_directory(directory)
    
    # check that n + 1 files remain in directory
    assert len(os.listdir(directory)) == days_of_history + 1
    
    # check that oldest file still exists in directory
    date = datetime.datetime.now().date() - datetime.timedelta(days=days_of_history)
    formatted_date = date.strftime("%Y-%m-%d")
    file_name = f"{directory}/{formatted_date}-log.txt"
    assert os.path.exists(file_name) == True
    
    # check that file one day older has been deleted
    date = datetime.datetime.now().date() - datetime.timedelta(days=days_of_history + 1)
    formatted_date = date.strftime("%Y-%m-%d")
    file_name = f"{directory}/{formatted_date}-log.txt"
    assert os.path.exists(file_name) == False
    
@freeze_time("2024-03-25 00:00:00")
def test_move_log_file(fs):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    os.makedirs(log_storage_path)
    destination_path = f"{log_storage_path}/{current_date}-log.txt"
    origin_path = log_file_name
    
    # Test when log file does not exist
    assert os.path.exists(destination_path) == False
    assert os.path.exists(origin_path) == False
    
    # Test when function is called and log file does not exist
    storage_manager._archive_latest_log_file()
    assert os.path.exists(destination_path) == False
    assert os.path.exists(origin_path) == False
    
    # Test when log file exists
    os.makedirs(log_file_name)
    assert os.path.exists(destination_path) == False
    assert os.path.exists(origin_path) == True
    
    # Test when function is called and log file exists
    storage_manager._archive_latest_log_file()
    assert os.path.exists(destination_path) == True
    assert os.path.exists(origin_path) == False