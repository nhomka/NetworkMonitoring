import datetime
import datetime_util
from freezegun import freeze_time
import os

os.environ['ENV'] = 'test'

@freeze_time("2024-03-25")
def test_current_date_string():
    assert datetime_util.current_date_string() == "2024-03-25"
    
@freeze_time("2024-03-25 00:00:00")
def test_date_to_remove_old_files():
    assert datetime_util.date_to_remove_old_files(28) == datetime.datetime.now().date() - datetime.timedelta(days=28)
    assert datetime_util.date_to_remove_old_files(28) < datetime.datetime.now().date() - datetime.timedelta(days=27)
    assert datetime_util.date_to_remove_old_files(28) > datetime.datetime.now().date() - datetime.timedelta(days=29)
    assert datetime_util.date_to_remove_old_files(0) == datetime.datetime.now().date()
    
@freeze_time("2024-03-25 23:59:59")
def test_is_start_of_day_before_start_of_day():
    assert datetime_util.is_start_of_day(10) == False
    assert datetime_util.is_start_of_day(60) == False
    assert datetime_util.is_start_of_day(180) == False
    assert datetime_util.is_start_of_day(235) == False
    
@freeze_time("2024-03-25 00:00:05")
def test_is_start_of_day_before_all_intervals():
    assert datetime_util.is_start_of_day(10) == True
    assert datetime_util.is_start_of_day(60) == True
    assert datetime_util.is_start_of_day(180) == True
    assert datetime_util.is_start_of_day(235) == True

@freeze_time("2024-03-25 00:00:30")
def test_is_start_of_day_after_an_interval():
    assert datetime_util.is_start_of_day(10) == False
    assert datetime_util.is_start_of_day(60) == True
    assert datetime_util.is_start_of_day(180) == True
    assert datetime_util.is_start_of_day(235) == True
    
@freeze_time("2024-03-25 00:2:59")
def test_is_start_of_day_after_greater_than_60_second_interval():
    assert datetime_util.is_start_of_day(10) == False
    assert datetime_util.is_start_of_day(60) == False
    assert datetime_util.is_start_of_day(180) == True
    assert datetime_util.is_start_of_day(235) == True
    
@freeze_time("2024-03-25 00:4:01")
def test_is_start_of_day_after_start_of_day():
    assert datetime_util.is_start_of_day(10) == False
    assert datetime_util.is_start_of_day(60) == False
    assert datetime_util.is_start_of_day(180) == False
    assert datetime_util.is_start_of_day(235) == False

def test_valid_get_date_from_log_file():
    parsed_date = datetime_util.get_date_from_log_file("2024-03-25-log.txt")
    assert parsed_date == datetime.date(2024, 3, 25)
    
@freeze_time("2024-03-25")
def test_invalid_get_date_from_log_file():
    parsed_date = datetime_util.get_date_from_log_file("log-2024-03-20-log.txt")
    assert parsed_date == datetime.date(2024, 3, 25)
    
@freeze_time("2024-03-25")
def test_wrong_format_get_date_from_log_file():
    parsed_date = datetime_util.get_date_from_log_file("03-20-2024-log.txt")
    assert parsed_date == datetime.date(2024, 3, 25)