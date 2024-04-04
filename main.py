from monitorconnection import NetworkMonitor
from pingsettings import PingSettings
import file_storage_configuration
from pinger import get_pinger_class

if __name__ == "__main__":
    settings = PingSettings()
    settings.pingAttempts = 5
    settings.interval = 60
    settings.host = "google.com"

    file_storage_configuration.initialize_storage()

    pinger = get_pinger_class(settings)
    monitor = NetworkMonitor(pinger)
    monitor.monitor_connection()