from typing import Any
from config.file_config import EmailInfo

class PingSettings:
    host = EmailInfo.HOST
    
    def __init__(self):
        self.pingAttempts = 4
        self.timeout = 2
        self.interval = 1
        self.packetSize = 32
        self.TTL = 128
        self.requiredSuccessfulPings = 1
        
    def __setattr__(self, name: str, value: Any) -> None:
        if name == "host":
            raise AttributeError("Host name must be changed through the private HostInfo class")
        super().__setattr__(name, value)
        
    def __str__(self) -> str:
        return f"Ping settings: {self.__dict__}"