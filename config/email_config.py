from config.private_configuration import SMTPInfo

class EmailInfo:
    SMTP_SERVER = SMTPInfo.SERVER
    SMTP_PORT = SMTPInfo.PORT
    SENDER_EMAIL = SMTPInfo.SENDER_EMAIL
    SENDER_PASSWORD = SMTPInfo.SENDER_PASSWORD
    RECIPIENT_EMAIL = SMTPInfo.RECIPIENT_EMAIL
    HOST = SMTPInfo.HOST
    
    SUBJECT_LINE = 'Daily Network Monitoring Report'
    MESSAGE_BODY = "Previous day's log file and charts are attached."