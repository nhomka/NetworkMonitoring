class pingsettings:
    def __init__(self):
        self.pingCount = 4
        self.pingTimeout = 2
        self.pingInterval = 1
        self.pingSize = 32
        self.pingTTL = 128
        self.pingType = "ICMP"
        self.pingHost = "www.google.com"