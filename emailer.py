from datetime import datetime
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from emailinfo import EmailInfo
from os.path import basename
from file_paths import log_file_name, success_storage_path, latency_storage_path

def send_email_report():
    message = _build_email_message()
    file_attachments = _get_file_attachments()
    _attach_files_to_message(message, file_attachments)
    _send_email(message)

# test-validated
def _build_email_message() -> MIMEMultipart:
    message = MIMEMultipart()
    message['From'] = EmailInfo.sender_email
    message['To'] = EmailInfo.receiver_email
    message['Subject'] = EmailInfo.subject_line

    body = EmailInfo.message_body
    message.attach(MIMEText(body, 'plain'))
    return message
    

def _get_file_attachments() -> list[str]:
    current_date = datetime.now().strftime("%Y-%m-%d")
    latency_chart_filename = f'{latency_storage_path}/{current_date}-ping_latency_chart.png'
    success_chart_filename = f'{success_storage_path}/{current_date}-ping_success_chart.png'
    return [log_file_name, latency_chart_filename, success_chart_filename]
    
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
        with smtplib.SMTP(EmailInfo.smtp_server, EmailInfo.smtp_port) as server:
            print(server)
            server.starttls()
            server.login(EmailInfo.sender_email, EmailInfo.sender_password)
            server.send_message(message)
        return True
    
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False