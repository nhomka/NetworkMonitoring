from monitorconnection import NetworkMonitor
from pingsettings import PingSettings
import file_storage_configuration

if __name__ == "__main__":
    settings = PingSettings()
    settings.pingAttempts = 5
    settings.interval = 60
    settings.host = "google.com"

    file_storage_configuration.initialize_storage()

    monitor = NetworkMonitor(settings)
    monitor.monitor_connection()