import platform
import pytest, pyfakefs
import os
from datetime import datetime, date
from monitorconnection import NetworkMonitor
from freezegun import freeze_time
import file_storage_configuration
from pingsettings import PingSettings
import datetime_functions

os.environ['ENV'] = 'test'
mockNetworkMonitor = NetworkMonitor()
mockPingSettings = PingSettings()

storage_directories = file_storage_configuration.storage_directories
log_storage_path = file_storage_configuration.log_storage_path

# Test cases for the NetworkMonitor class
@freeze_time("2024-03-25")
def test_get_current_date_string():
    assert datetime_functions.current_date_string() == "2024-03-25"

def test_valid_get_date_from_log_file():
    parsed_date = datetime_functions.get_date_from_log_file("2024-03-25-log.txt")
    assert parsed_date == date(2024, 3, 25)
    
@freeze_time("2024-03-25")
def test_invalid_get_date_from_log_file():
    parsed_date = datetime_functions.get_date_from_log_file("log-2024-03-20-log.txt")
    assert parsed_date == date(2024, 3, 25)
    
@freeze_time("2024-03-25")
def test_wrong_format_get_date_from_log_file():
    parsed_date = datetime_functions.get_date_from_log_file("03-20-2024-log.txt")
    assert parsed_date == date(2024, 3, 25)
    
def test_on_creation_check_storage_directories(fs):
    for path in storage_directories:
        assert os.path.exists(path) == False
    file_storage_configuration.check_storage_paths()
    for path in storage_directories:
        assert os.path.exists(path) == True
    
@freeze_time("2024-03-25 00:00:00")
def test_move_log_file(fs):
    current_date = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(log_storage_path)
    destination_path = f"{log_storage_path}/{current_date}-log.txt"
    origin_path = "log.txt"
    
    # Test when log file does not exist
    assert os.path.exists(destination_path) == False
    assert os.path.exists(origin_path) == False
    
    # Test when function is called and log file does not exist
    file_storage_configuration.move_log_file()
    assert os.path.exists(destination_path) == False
    assert os.path.exists(origin_path) == False
    
    # Test when log file exists
    os.makedirs("log.txt")
    assert os.path.exists(destination_path) == False
    assert os.path.exists(origin_path) == True
    
    # Test when function is called and log file exists
    file_storage_configuration.move_log_file()
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
    