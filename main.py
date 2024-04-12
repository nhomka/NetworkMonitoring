from monitorconnection import NetworkMonitor
from config.pingsettings import PingSettings
from file_manager import initialize_storage
from config.private_configuration import SMTPInfo
from config.file_config import FileSystemInfo as fs
import time

if __name__ == "__main__":
    # settings = PingSettings()
    # settings.pingAttempts = 5
    # settings.interval = 60
    # settings.host = "google.com"

    # initialize_storage()

    hosts = SMTPInfo.HOST_DICTIONARY
    
    monitors = []
    
    for address, friendly_name in hosts.items():
        settings = PingSettings()
        settings.host = address
        settings.friendly_name = friendly_name
        
        monitor = NetworkMonitor(settings)
        
        initialize_storage(monitor.file_system_config)
        monitors.append(monitor)
            
    while True:
        for monitor in monitors:
            monitor.monitor_connections()
            
        time.sleep(60)

    # monitor = NetworkMonitor(settings)
    # monitor.monitor_connections()