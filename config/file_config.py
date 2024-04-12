import os
    
class FileSystemInfo:
    FRIENDLY_HOST_NAME = "DefaultHost"
    
    DAYS_OF_HISTORY = 28
    DAYS_OF_HISTORY_PER_FILE = 1

    BASE_STORAGE_PATH = os.environ["HOMEPATH"] if os.name == "nt" else os.environ["HOME"]
    APP_STORAGE_PATH = f"{BASE_STORAGE_PATH}\\NetworkMonitor"
    
    HOST_STORAGE_PATH = f"{APP_STORAGE_PATH}\\{FRIENDLY_HOST_NAME}"

    PLOTS_STORAGE_PATH = HOST_STORAGE_PATH + "\\Plots"
    LATENCY_STORAGE_PATH = HOST_STORAGE_PATH + "\\Plots\\Latency"
    SUCCESS_STORAGE_PATH = HOST_STORAGE_PATH + "\\Plots\\Success"
    LOG_STORAGE_PATH = HOST_STORAGE_PATH + "\\Logs"
    LOG_FILE_NAME = HOST_STORAGE_PATH + "\\Logs\\log.txt"

    STORAGE_DIRECTORIES = [LATENCY_STORAGE_PATH, SUCCESS_STORAGE_PATH, LOG_STORAGE_PATH]
    
    def __init__(self, name:str = "www.google.com") -> None:
        self.FRIENDLY_HOST_NAME = name
        self.HOST_STORAGE_PATH = f"{self.APP_STORAGE_PATH}\\{self.FRIENDLY_HOST_NAME}"

        self.PLOTS_STORAGE_PATH = self.HOST_STORAGE_PATH + "\\Plots"
        self.LATENCY_STORAGE_PATH = self.HOST_STORAGE_PATH + "\\Plots\\Latency"
        self.SUCCESS_STORAGE_PATH = self.HOST_STORAGE_PATH + "\\Plots\\Success"
        self.LOG_STORAGE_PATH = self.HOST_STORAGE_PATH + "\\Logs"
        self.LOG_FILE_NAME = self.HOST_STORAGE_PATH + "\\Logs\\log.txt"

        self.STORAGE_DIRECTORIES = [self.LATENCY_STORAGE_PATH, self.SUCCESS_STORAGE_PATH, self.LOG_STORAGE_PATH]