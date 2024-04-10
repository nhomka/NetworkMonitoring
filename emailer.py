from config.email_config import EmailInfo
from config.file_config import FileSystemInfo as fs
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
import smtplib

def send_email_report():
    message = _build_email_message()
    file_attachments = _get_file_attachments()
    _attach_files_to_message(message, file_attachments)
    _send_email(message)

# test-validated
def _build_email_message() -> MIMEMultipart:
    message = MIMEMultipart()
    message['From'] = EmailInfo.SENDER_EMAIL
    message['To'] = EmailInfo.RECIPIENT_EMAIL
    message['Subject'] = EmailInfo.SUBJECT_LINE

    body = EmailInfo.MESSAGE_BODY
    message.attach(MIMEText(body, 'plain'))
    return message
    

def _get_file_attachments() -> list[str]:
    current_date = datetime.now().strftime("%Y-%m-%d")
    latency_chart_filename = f'{fs.LATENCY_STORAGE_PATH}/{current_date}-ping_latency_chart.png'
    success_chart_filename = f'{fs.SUCCESS_STORAGE_PATH}/{current_date}-ping_success_chart.png'
    return [fs.LOG_FILE_NAME, latency_chart_filename, success_chart_filename]
    
def _attach_files_to_message(message: MIMEMultipart, file_attachments: list[str]) -> None:
    for file in file_attachments:
        with open(file, "rb") as f:
            part = MIMEApplication(
                f.read(),
                Name=basename(file)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
        message.attach(part)
        
def _send_email(message: MIMEMultipart) -> bool:
    try:
        with smtplib.SMTP(EmailInfo.SMTP_SERVER, EmailInfo.SMTP_PORT) as server:
            print(server)
            server.starttls()
            server.login(EmailInfo.SENDER_EMAIL, EmailInfo.SENDER_PASSWORD)
            server.send_message(message)
        return True
    
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False