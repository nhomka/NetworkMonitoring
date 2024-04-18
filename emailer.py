from config.email_config import EmailInfo
from config.file_config import FileSystemInfo
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
import smtplib

class Emailer:
    def __init__(self, fs: FileSystemInfo):
        self.fs = fs

    def send_email_report(self):
        message = self._build_email_message()
        file_attachments = self._get_file_attachments()
        self._attach_files_to_message(message, file_attachments)
        self._send_email(message)

    def _build_email_message(self) -> MIMEMultipart:
        message = MIMEMultipart()
        message['From'] = EmailInfo.SENDER_EMAIL
        message['To'] = EmailInfo.RECIPIENT_EMAIL
        message['Subject'] = EmailInfo.SUBJECT_LINE

        body = EmailInfo.MESSAGE_BODY
        message.attach(MIMEText(body, 'plain'))
        return message

    def _get_file_attachments(self) -> list[str]:
        current_date = datetime.now().strftime("%Y-%m-%d")
        latency_chart_filename = f'{self.fs.LATENCY_STORAGE_PATH}/{current_date}-ping_latency_chart.png'
        success_chart_filename = f'{self.fs.SUCCESS_STORAGE_PATH}/{current_date}-ping_success_chart.png'
        return [self.fs.LOG_FILE_NAME, latency_chart_filename, success_chart_filename]

    def _attach_files_to_message(self, message: MIMEMultipart, file_attachments: list[str]) -> None:
        for file in file_attachments:
            with open(file, "rb") as f:
                part = MIMEApplication(
                    f.read(),
                    Name=basename(file)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
            message.attach(part)

    def _send_email(self, message: MIMEMultipart) -> bool:
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