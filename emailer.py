import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from EmailInfo import EmailInfo

smtp_server = EmailInfo.smtp_server
smtp_port = EmailInfo.smtp_port
sender_email = EmailInfo.sender_email
sender_password = EmailInfo.sender_password
receiver_email = EmailInfo.receiver_email

message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = 'Daily Network Monitoring Report'

body = "Previous day's log file and charts are attacked."
message.attach(MIMEText(body, 'plain'))

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(message)

print("Email sent successfully")