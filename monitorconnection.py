import time
from datetime import datetime
from config.pingsettings import PingSettings
from config.file_config import FileSystemInfo
from file_manager import clean_old_logs, move_log_file
from datetime_helper import is_start_of_day
from pinger import get_pinger_class
import emailer
import plotter

class NetworkMonitor:
    def __init__(self, pingsettings = PingSettings()):
        self.settings = pingsettings
        self.pinger = get_pinger_class(self.settings.host)
        self.file_system_config = FileSystemInfo(self.settings.friendly_name)

    def monitor_connections(self):
        success, latency = self.pinger.ping()
        self._log_results(success, latency)

        if is_start_of_day(self.settings.interval):
            plotter.build_charts(self.file_system_config)
            emailer.send_email_report(self.file_system_config)
            move_log_file(self.file_system_config)
            clean_old_logs(self.file_system_config)

    def _log_results(self, success: bool, latency: float) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        friendly_name = self.settings.friendly_name
        
        with open(self.file_system_config.LOG_FILE_NAME, "a") as file:
            file.write(f"{friendly_name},{timestamp},{success},{latency:0f}\n")