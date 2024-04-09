from private_configuration import SMTPInfo, HostInfo
import os

class EmailInfo:
    SMTP_SERVER = SMTPInfo.SERVER
    SMTP_PORT = SMTPInfo.PORT
    SENDER_EMAIL = SMTPInfo.SENDER_EMAIL
    SENDER_PASSWORD = SMTPInfo.SENDER_PASSWORD
    RECIPIENT_EMAIL = SMTPInfo.RECIPIENT_EMAIL
    HOST = HostInfo.HOST
    
    SUBJECT_LINE = 'Daily Network Monitoring Report'
    MESSAGE_BODY = "Previous day's log file and charts are attached."
    
class FileSystemInfo:
    DAYS_OF_HISTORY = 28
    DAYS_OF_HISTORY_PER_FILE = 1

    BASE_STORAGE_PATH = os.environ["HOMEPATH"] if os.name == "nt" else os.environ["HOME"]
    APP_STORAGE_PATH = f"{BASE_STORAGE_PATH}\\NetworkMonitor"

    PLOTS_STORAGE_PATH = APP_STORAGE_PATH + "\\Plots"
    LATENCY_STORAGE_PATH = APP_STORAGE_PATH + "\\Plots\\Latency"
    SUCCESS_STORAGE_PATH = APP_STORAGE_PATH + "\\Plots\\Success"
    LOG_STORAGE_PATH = APP_STORAGE_PATH + "\\Logs"
    LOG_FILE_NAME = APP_STORAGE_PATH + "\\Logs\\log.txt"

    STORAGE_DIRECTORIES = [LATENCY_STORAGE_PATH, SUCCESS_STORAGE_PATH, LOG_STORAGE_PATH]