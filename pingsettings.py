class PingSettings:
    def __init__(self):
        self.pingAttempts = 4
        self.timeout = 2
        self.interval = 1
        self.packetSize = 32
        self.TTL = 128
        self.host = "www.google.com"
        self.requiredSuccessfulPings = 1