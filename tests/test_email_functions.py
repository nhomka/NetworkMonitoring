from email.mime.multipart import MIMEMultipart
import pytest, pyfakefs
from unittest.mock import patch, MagicMock
import os
import datetime
from freezegun import freeze_time
from emailer import Emailer
from config.file_config import FileSystemInfo
from config.email_config import EmailInfo

os.environ['ENV'] = 'test'
file_system_info = FileSystemInfo()
emailer = Emailer(file_system_info)

def test_build_email_message():
    test_message = emailer._build_email_message()
    assert test_message['From'] == EmailInfo.SENDER_EMAIL
    assert test_message['To'] == EmailInfo.RECIPIENT_EMAIL
    assert test_message['Subject'] == EmailInfo.SUBJECT_LINE
    assert test_message.get_payload()[0].get_payload() == EmailInfo.MESSAGE_BODY
    
@freeze_time("2024-03-25")
def test_get_file_attachments():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    latency_chart_filename = f'{file_system_info.LATENCY_STORAGE_PATH}/{current_date}-ping_latency_chart.png'
    success_chart_filename = f'{file_system_info.SUCCESS_STORAGE_PATH}/{current_date}-ping_success_chart.png'
    
    attachments = emailer._get_file_attachments()
    
    assert len(attachments) == 3
    assert file_system_info.LOG_FILE_NAME in attachments
    assert latency_chart_filename in attachments
    assert success_chart_filename in attachments

def test_attach_files_to_message(fs):
    message = MIMEMultipart()
    file_attachments = ["test1.txt", "test2.txt", "test3.txt"]
    
    for file in file_attachments:
        fs.create_file(file)
    
    emailer._attach_files_to_message(message, file_attachments)
    
    assert len(message.get_payload()) == 3
    for i, attachment in enumerate(message.get_payload()):
        assert attachment.get_filename() == file_attachments[i]
        assert attachment.get_content_disposition() == 'attachment'    

# @pytest.fixture
# def smtp_mock():
#     with patch('emailer.smtplib.SMTP') as mock_smtplib:
#         yield mock_smtplib

# def test_send_email_success(smtp_mock):
#     # Configure mock behavior
#     mock_smtp_instance = MagicMock()
#     smtp_mock.return_value = mock_smtp_instance
#     mock_smtp_instance.send_message.return_value = (None, {})

#     # Call the function to send email
#     message = emailer.build_email_message()
#     result = emailer.send_email(message)

#     # Assert that the email was sent successfully
#     assert result is True
#     smtp_mock.assert_called_once_with(EmailInfo.smtp_server, EmailInfo.smtp_port)
    
#     mock_smtp_instance.starttls.assert_called_once()
#     mock_smtp_instance.login.assert_called_once_with(EmailInfo.sender_email, EmailInfo.sender_password)
#     mock_smtp_instance.send_message.assert_called_once()
    
# def test_send_email_failure(smtp_mock):
#     # Configure mock behavior
#     mock_smtp_instance = MagicMock()
#     smtp_mock.SMTP.return_value = mock_smtp_instance
#     mock_smtp_instance.send_message.side_effect = Exception("Email sending failed")

#     # Call the function to send email
#     message = emailer.build_email_message()
#     result = emailer.send_email(message)

#     # Assert that the email sending failed
#     assert result is False
#     smtp_mock.SMTP.assert_called_once_with(EmailInfo.smtp_server, EmailInfo.smtp_port)
#     mock_smtp_instance.login.assert_called_once_with(EmailInfo.sender_email, EmailInfo.sender_password)
#     mock_smtp_instance.send_message.assert_called_once()