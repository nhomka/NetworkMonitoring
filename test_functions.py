import pytest, pyfakefs
import os
from datetime import datetime, date
from monitorconnection import NetworkMonitor
from freezegun import freeze_time
from storageconfig import StorageConfig

os.environ['ENV'] = 'test'
mockNetworkMonitor = NetworkMonitor()


# Test cases for the NetworkMonitor class
@freeze_time("2024-03-25")
def test_get_current_date_string():
    assert mockNetworkMonitor.get_current_date_string() == "2024-03-25"

def test_valid_get_date_from_log_file():
    parsed_date = mockNetworkMonitor.get_date_from_log_file("2024-03-25-log.txt")
    assert parsed_date == date(2024, 3, 25)
    
@freeze_time("2024-03-25")
def test_invalid_get_date_from_log_file():
    parsed_date = mockNetworkMonitor.get_date_from_log_file("log-2024-03-20-log.txt")
    assert parsed_date == date(2024, 3, 25)
    
@freeze_time("2024-03-25")
def test_wrong_format_get_date_from_log_file():
    parsed_date = mockNetworkMonitor.get_date_from_log_file("03-20-2024-log.txt")
    assert parsed_date == date(2024, 3, 25)
    
def test_on_creation_check_storage_directories(fs):
    for path in [StorageConfig.log_storage_path, StorageConfig.latency_storage_path, StorageConfig.success_storage_path]:
        assert os.path.exists(path) == False
    mockNetworkMonitor.check_storage_paths()
    for path in [StorageConfig.log_storage_path, StorageConfig.latency_storage_path, StorageConfig.success_storage_path]:
        assert os.path.exists(path) == True