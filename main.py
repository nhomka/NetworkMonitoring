from monitorconnection import NetworkMonitor
from pingsettings import PingSettings

if __name__ == "__main__":
    settings = PingSettings()
    settings.pingCount = 5
    settings.pingInterval = 60
    settings.pingHost = "google.com"

    monitor = NetworkMonitor(settings)
    monitor.monitor_connection()