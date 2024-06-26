import platform, os

# Project - understand how to better enforce this as an interface

def get_pinger_class(host: str = "www.google.com") -> 'Pinger':
    if platform.system().lower() == "windows":
        return WindowsPinger(host)
    else:
        return LinuxPinger(host)

class Pinger:
    def __init__(self, host: str):
        self.host = host

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
    def __init__(self, host: str):
        super().__init__(host)
    
    def _get_ping_command(self) -> str:
        return f"ping -n 1 {self.host}"
    
    def _is_ping_successful(self, ping_response: str) -> bool:
        return "Reply from" in ping_response
    
    def _get_latency(self, response: str) -> float:
        return float(response.split("Average = ")[1].split("ms")[0])
    
class LinuxPinger(Pinger):
    def __init__(self, host: str):
        super().__init__(host)
        
    def _get_ping_command(self) -> str:
        return f"ping -c 1 {self.host}"
    
    def _is_ping_successful(self, ping_response: str) -> bool:
        return "1 packets transmitted, 1 received" in ping_response
    
    def _get_latency(self, response: str) -> float:
        return float(response.split("time=")[1].split(" ")[0])