import os
import platform
import pytest, pyfakefs
from pingsettings import PingSettings
from pinger import get_pinger_class
from hostinfo import HostInfo

os.environ['ENV'] = 'test'
mockPingSettings = PingSettings()
    
def test_get_ping_command_windows():
    platform.system = lambda: "Windows"
    mockPinger = get_pinger_class(mockPingSettings)
    assert mockPinger._get_ping_command() == f"ping -n 1 {HostInfo.hostname}"
    
def test_get_ping_command_linux():
    platform.system = lambda: "Linux"
    mockPinger = get_pinger_class(mockPingSettings)
    assert mockPinger._get_ping_command() == f"ping -c 1 {HostInfo.hostname}"