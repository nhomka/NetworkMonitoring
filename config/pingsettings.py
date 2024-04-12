from typing import Any
from config.private_configuration import SMTPInfo

class PingSettings:
    host = SMTPInfo.HOST
    
    def __init__(self):
        self.pingAttempts = 4
        self.timeout = 2
        self.interval = 1
        self.packetSize = 32
        self.TTL = 128
        self.requiredSuccessfulPings = 1
        
    def __setattr__(self, name: str, value: Any) -> None:
        if name == "host":
            raise AttributeError("Host name must be changed through the private SMTPInfo class")
        super().__setattr__(name, value)
        
    def __str__(self) -> str:
        return f"Ping settings: {self.__dict__}"