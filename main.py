from monitorconnection import NetworkMonitor
from config.pingsettings import PingSettings
from config.private_configuration import SMTPInfo
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
        
        # I need to not sleep - continuously run the loop and check within each monitor if it is time to ping
        # Currently can't enforce custom intervals for each monitor
        time.sleep(60)