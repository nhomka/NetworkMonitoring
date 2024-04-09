from monitorconnection import NetworkMonitor
from pingsettings import PingSettings
from file_storage_configuration import initialize_storage

if __name__ == "__main__":
    settings = PingSettings()
    settings.pingAttempts = 5
    settings.interval = 60
    settings.host = "google.com"

    initialize_storage()

    monitor = NetworkMonitor(settings)
    monitor.monitor_connection()