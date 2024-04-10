import os
import platform
import pytest, pyfakefs
from config.pingsettings import PingSettings
from pinger import get_pinger_class
from config.file_config import EmailInfo

os.environ['ENV'] = 'test'
mockPingSettings = PingSettings()
    
def test_get_ping_command_windows():
    platform.system = lambda: "Windows"
    mockPinger = get_pinger_class(mockPingSettings)
    assert mockPinger._get_ping_command() == f"ping -n 1 {EmailInfo.HOST}"
    
def test_get_ping_command_linux():
    platform.system = lambda: "Linux"
    mockPinger = get_pinger_class(mockPingSettings)
    assert mockPinger._get_ping_command() == f"ping -c 1 {EmailInfo.HOST}"