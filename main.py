from src.network_monitor import NetworkMonitor
from src.config.pingsettings import PingSettings
from src.config.private_configuration import SMTPInfo
import time

if __name__ == "__main__":
    
    hosts = SMTPInfo.HOST_DICTIONARY
    
    monitors = []
    
    for address, friendly_name in hosts.items():
        settings = PingSettings()
        settings.host = address
        settings.friendly_name = friendly_name
        
        monitor = NetworkMonitor(settings)
        monitors.append(monitor)
            
    while True:
        for monitor in monitors:
            monitor.monitor_connections()