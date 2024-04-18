from datetime import datetime, timedelta

#test-validated
def current_date_string() -> str:
    return datetime.now().strftime("%Y-%m-%d")

#test-validated
def date_to_remove_old_files(days_to_subtract: int) -> datetime.date:
    return datetime.now().date() - timedelta(days=days_to_subtract)

#test-validated
def is_start_of_day(delay_secs: int) -> bool:
    current_time = datetime.now()
    return \
        current_time <= datetime.now().replace(hour=0, minute=(delay_secs//60), second = delay_secs % 60) \
        and current_time >= datetime.now().replace(hour=0, minute=0, second = 0)
        
#test-validated
def get_date_from_log_file(log_file_name: str) -> datetime.date:
    try:
        file_date = datetime.strptime(log_file_name[:10], "%Y-%m-%d").date()
        return file_date
    except:
        return datetime.now().date()