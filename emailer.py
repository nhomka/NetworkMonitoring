from datetime import datetime
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from EmailInfo import EmailInfo
from os.path import basename
from file_storage_configuration import log_file_name, success_storage_path, latency_storage_path

smtp_server = EmailInfo.smtp_server
smtp_port = EmailInfo.smtp_port
sender_email = EmailInfo.sender_email
sender_password = EmailInfo.sender_password
receiver_email = EmailInfo.receiver_email

def send_email_report():

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Daily Network Monitoring Report'

    body = "Previous day's log file and charts are attached."
    message.attach(MIMEText(body, 'plain'))

    file_attachments = get_file_attachments()

    for file in file_attachments:
        with open(file, "rb") as f:
            part = MIMEApplication(
                f.read(),
                Name=basename(file)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
        message.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

    print("Email sent successfully")
    
def get_file_attachments():
    current_date = datetime.now().strftime("%Y-%m-%d")
    return [log_file_name,
            f'{latency_storage_path}/{current_date}-ping_latency_chart.png',
            f'{success_storage_path}/{current_date}-ping_success_chart.png']