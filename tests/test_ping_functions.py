import os
import platform
import pytest, pyfakefs
from config.pingsettings import PingSettings
from src.pinger import get_pinger_class

os.environ['ENV'] = 'test'
mockPingSettings = PingSettings()
    
def test_get_ping_command_windows():
    platform.system = lambda: "Windows"
    mockPinger = get_pinger_class(mockPingSettings.host)
    assert mockPinger._get_ping_command() == f"ping -n 1 {mockPingSettings.host}"
    
def test_get_ping_command_linux():
    platform.system = lambda: "Linux"
    mockPinger = get_pinger_class(mockPingSettings.host)
    assert mockPinger._get_ping_command() == f"ping -c 1 {mockPingSettings.host}"