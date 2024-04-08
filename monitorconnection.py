import time
from datetime import datetime
from pingsettings import PingSettings
from file_paths import log_file_name
from file_storage_configuration import clean_old_logs, move_log_file
from datetime_functions import is_start_of_day
from pinger import get_pinger_class
import emailer
import plot_builder

class NetworkMonitor:
    def __init__(self, pingsettings = PingSettings()):
        self.settings = pingsettings
        self.pinger = get_pinger_class(self.settings)

    def monitor_connection(self):
        while True:
            success, latency = self.pinger.ping()
            self._log_results(success, latency)

            if is_start_of_day(self.settings.interval):
                plot_builder.build_charts()
                emailer.send_email_report()
                move_log_file()
                clean_old_logs()

            time.sleep(self.settings.interval)  # Wait for the remaining time in the interval

    def _log_results(self, success: bool, latency: float) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file_name, "a") as file:
            file.write(f"{timestamp},{success},{latency:0f}\n")