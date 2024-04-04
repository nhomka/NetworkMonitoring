import platform
import pytest, pyfakefs
import os
import datetime
from monitorconnection import NetworkMonitor
from freezegun import freeze_time
import file_storage_configuration
from pingsettings import PingSettings
import datetime_functions
from pinger import get_pinger_class

os.environ['ENV'] = 'test'
mockPingSettings = PingSettings()
mockPinger = get_pinger_class(mockPingSettings)
mockNetworkMonitor = NetworkMonitor()

storage_directories = file_storage_configuration.storage_directories
log_storage_path = file_storage_configuration.log_storage_path
log_file_name = file_storage_configuration.log_file_name

# Test cases for the NetworkMonitor class
@freeze_time("2024-03-25")
def test_current_date_string():
    assert datetime_functions.current_date_string() == "2024-03-25"

def test_valid_get_date_from_log_file():
    parsed_date = datetime_functions.get_date_from_log_file("2024-03-25-log.txt")
    assert parsed_date == datetime.date(2024, 3, 25)
    
@freeze_time("2024-03-25")
def test_invalid_get_date_from_log_file():
    parsed_date = datetime_functions.get_date_from_log_file("log-2024-03-20-log.txt")
    assert parsed_date == datetime.date(2024, 3, 25)
    
@freeze_time("2024-03-25")
def test_wrong_format_get_date_from_log_file():
    parsed_date = datetime_functions.get_date_from_log_file("03-20-2024-log.txt")
    assert parsed_date == datetime.date(2024, 3, 25)
    
def test_on_creation_check_storage_directories(fs):
    for path in storage_directories:
        assert os.path.exists(path) == False
    file_storage_configuration.check_storage_paths()
    for path in storage_directories:
        assert os.path.exists(path) == True
    
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
    file_storage_configuration.move_log_file()
    assert os.path.exists(destination_path) == False
    assert os.path.exists(origin_path) == False
    
    # Test when log file exists
    os.makedirs(log_file_name)
    assert os.path.exists(destination_path) == False
    assert os.path.exists(origin_path) == True
    
    # Test when function is called and log file exists
    file_storage_configuration.move_log_file()
    assert os.path.exists(destination_path) == True
    assert os.path.exists(origin_path) == False
    
def test_get_ping_command_windows():
    platform.system = lambda: "Windows"
    mockPinger = get_pinger_class(mockPingSettings)
    assert mockPinger._get_ping_command() == f"ping -n 1 www.google.com"
    
def test_get_ping_command_linux():
    platform.system = lambda: "Linux"
    mockPinger = get_pinger_class(mockPingSettings)
    assert mockPinger._get_ping_command() == f"ping -c 1 www.google.com"
    
def test_date_to_remove_old_files():
    assert datetime_functions.date_to_remove_old_files(28) == datetime.datetime.now().date() - datetime.timedelta(days=28)
    assert datetime_functions.date_to_remove_old_files(28) < datetime.datetime.now().date() - datetime.timedelta(days=27)
    assert datetime_functions.date_to_remove_old_files(28) > datetime.datetime.now().date() - datetime.timedelta(days=29)
    assert datetime_functions.date_to_remove_old_files(0) == datetime.datetime.now().date()
    
@freeze_time("2024-03-25 23:59:59")
def test_is_start_of_day_before_start_of_day():
    assert datetime_functions.is_start_of_day(10) == False
    assert datetime_functions.is_start_of_day(60) == False
    assert datetime_functions.is_start_of_day(180) == False
    assert datetime_functions.is_start_of_day(235) == False
    
@freeze_time("2024-03-25 00:00:05")
def test_is_start_of_day_before_all_intervals():
    assert datetime_functions.is_start_of_day(10) == True
    assert datetime_functions.is_start_of_day(60) == True
    assert datetime_functions.is_start_of_day(180) == True
    assert datetime_functions.is_start_of_day(235) == True

@freeze_time("2024-03-25 00:00:30")
def test_is_start_of_day_after_an_interval():
    assert datetime_functions.is_start_of_day(10) == False
    assert datetime_functions.is_start_of_day(60) == True
    assert datetime_functions.is_start_of_day(180) == True
    assert datetime_functions.is_start_of_day(235) == True
    
@freeze_time("2024-03-25 00:2:59")
def test_is_start_of_day_after_greater_than_60_second_interval():
    assert datetime_functions.is_start_of_day(10) == False
    assert datetime_functions.is_start_of_day(60) == False
    assert datetime_functions.is_start_of_day(180) == True
    assert datetime_functions.is_start_of_day(235) == True
    
@freeze_time("2024-03-25 00:4:01")
def test_is_start_of_day_after_start_of_day():
    assert datetime_functions.is_start_of_day(10) == False
    assert datetime_functions.is_start_of_day(60) == False
    assert datetime_functions.is_start_of_day(180) == False
    assert datetime_functions.is_start_of_day(235) == False