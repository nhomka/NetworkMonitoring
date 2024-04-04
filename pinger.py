import platform, os
from pingsettings import PingSettings

def get_pinger_class(pingsettings = PingSettings()):
    if platform.system().lower() == "windows":
        return WindowsPinger(pingsettings)
    else:
        return LinuxPinger(pingsettings)

class Pinger:
    def __init__(self, pingsettings = PingSettings()):
        self.settings = pingsettings

    def ping(self):
        ping_command = self._get_ping_command()
        response = self._send_ping_command(ping_command)
        success = self._is_ping_successful(response)
        latency = self._get_latency(response) if success else 0
        return success, latency

    #test-validated
    def _get_ping_command(self):
        pass

    def _send_ping_command(self, ping_command):
        response = os.popen(ping_command).read()
        return response

    def _is_ping_successful(self, ping_response):
        pass

    def _get_latency(ping_str):
        pass
    
class WindowsPinger(Pinger):
    def __init__(self, pingsettings = PingSettings()):
        super().__init__(pingsettings)
    
    def _get_ping_command(self):
        return f"ping -n 1 {self.settings.host}"
    
    def _is_ping_successful(self, ping_response):
        return "Reply from" in ping_response
    
    def _get_latency(self, response):
        return float(response.split("Average = ")[1].split("ms")[0])
    
class LinuxPinger(Pinger):
    def __init__(self, pingsettings = PingSettings()):
        super().__init__(pingsettings)
        
    def _get_ping_command(self):
        return f"ping -c 1 {self.settings.host}"
    
    def _is_ping_successful(self, ping_response):
        return "1 packets transmitted, 1 received" in ping_response
    
    def _get_latency(self, response):
        return float(response.split("time=")[1].split(" ")[0])