import platform
import pytest, pyfakefs
import os
from datetime import datetime, date
from monitorconnection import NetworkMonitor
from freezegun import freeze_time
from storageconfig import StorageConfig
from pingsettings import PingSettings

os.environ['ENV'] = 'test'
mockNetworkMonitor = NetworkMonitor()
mockPingSettings = PingSettings()

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
    
@freeze_time("2024-03-25 00:00:00")
def test_move_log_file(fs):
    current_date = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(StorageConfig.log_storage_path)
    destination_path = f"{StorageConfig.log_storage_path}/{current_date}-log.txt"
    origin_path = "log.txt"
    
    # Test when log file does not exist
    assert os.path.exists(destination_path) == False
    assert os.path.exists(origin_path) == False
    
    # Test when function is called and log file does not exist
    mockNetworkMonitor.move_log_file()
    assert os.path.exists(destination_path) == False
    assert os.path.exists(origin_path) == False
    
    # Test when log file exists
    os.makedirs("log.txt")
    assert os.path.exists(destination_path) == False
    assert os.path.exists(origin_path) == True
    
    # Test when function is called and log file exists
    mockNetworkMonitor.move_log_file()
    assert os.path.exists(destination_path) == True
    assert os.path.exists(origin_path) == False
    
def test_build_ping_string_windows():
    platform.system = lambda: "Windows"
    assert mockNetworkMonitor.build_ping_command() == f"ping -n 1 www.google.com"
    
def test_build_ping_string_linux():
    platform.system = lambda: "Linux"
    assert mockNetworkMonitor.build_ping_command() == f"ping -c 1 www.google.com"
    
def test_get_os_specific_ping_string_windows():
    platform.system = lambda: "Windows"
    assert mockNetworkMonitor.get_os_specific_ping() == "-n 1"
    
def test_get_os_specific_ping_string_linux():
    platform.system = lambda: "Linux"
    assert mockNetworkMonitor.get_os_specific_ping() == "-c 1"
    