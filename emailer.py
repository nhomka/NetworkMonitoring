from datetime import datetime
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from EmailInfo import EmailInfo
from os.path import basename
from file_paths import log_file_name, success_storage_path, latency_storage_path

def send_email_report():
    message = build_email_message()
    file_attachments = get_file_attachments()
    attach_files_to_email(message, file_attachments)
    send_email(message)

def build_email_message():
    message = MIMEMultipart()
    message['From'] = EmailInfo.sender_email
    message['To'] = EmailInfo.receiver_email
    message['Subject'] = 'Daily Network Monitoring Report'

    body = "Previous day's log file and charts are attached."
    message.attach(MIMEText(body, 'plain'))
    return message
    
def get_file_attachments():
    current_date = datetime.now().strftime("%Y-%m-%d")
    return [log_file_name,
            f'{latency_storage_path}/{current_date}-ping_latency_chart.png',
            f'{success_storage_path}/{current_date}-ping_success_chart.png']
    
def attach_files_to_email(message, file_attachments):
    for file in file_attachments:
        with open(file, "rb") as f:
            part = MIMEApplication(
                f.read(),
                Name=basename(file)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
        message.attach(part)
        
def send_email(message):
    with smtplib.SMTP(EmailInfo.smtp_server, EmailInfo.smtp_port) as server:
        server.starttls()
        server.login(EmailInfo.sender_email, EmailInfo.sender_password)
        server.send_message(message)

    print("Email sent successfully")