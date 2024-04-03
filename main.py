from monitorconnection import NetworkMonitor
from pingsettings import PingSettings
import file_storage_configuration

if __name__ == "__main__":
    settings = PingSettings()
    settings.pingCount = 5
    settings.pingInterval = 60
    settings.pingHost = "google.com"

    file_storage_configuration.initialize_storage()

    monitor = NetworkMonitor(settings)
    monitor.monitor_connection()