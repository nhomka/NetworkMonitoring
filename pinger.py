import platform, os
from config.pingsettings import PingSettings

# Project - understand how to better enforce this as an interface

def get_pinger_class(pingsettings = PingSettings()) -> 'Pinger':
    if platform.system().lower() == "windows":
        return WindowsPinger(pingsettings)
    else:
        return LinuxPinger(pingsettings)

class Pinger:
    def __init__(self, pingsettings = PingSettings()):
        self.settings = pingsettings

    def ping(self) -> tuple[bool, float]:
        ping_command = self._get_ping_command()
        response = self._send_ping_command(ping_command)
        success = self._is_ping_successful(response)
        latency = self._get_latency(response) if success else 0
        return success, latency

    def _send_ping_command(self, ping_command: str) -> str:
        response = os.popen(ping_command).read()
        print(response)
        return response
        
    def _get_ping_command(self) -> str:
        raise NotImplementedError("Subclasses must implement this method")    
        
    def _is_ping_successful(self, ping_response: str) -> bool:
        raise NotImplementedError("Subclasses must implement this method")
    
    def _get_latency(self, response: str) -> float:
        raise NotImplementedError("Subclasses must implement this method")
    
class WindowsPinger(Pinger):
    def __init__(self, pingsettings = PingSettings()):
        super().__init__(pingsettings)
    
    def _get_ping_command(self) -> str:
        return f"ping -n 1 {self.settings.host}"
    
    def _is_ping_successful(self, ping_response: str) -> bool:
        return "Reply from" in ping_response
    
    def _get_latency(self, response: str) -> float:
        return float(response.split("Average = ")[1].split("ms")[0])
    
class LinuxPinger(Pinger):
    def __init__(self, pingsettings = PingSettings()):
        super().__init__(pingsettings)
        
    def _get_ping_command(self) -> str:
        return f"ping -c 1 {self.settings.host}"
    
    def _is_ping_successful(self, ping_response: str) -> bool:
        return "1 packets transmitted, 1 received" in ping_response
    
    def _get_latency(self, response: str) -> float:
        return float(response.split("time=")[1].split(" ")[0])