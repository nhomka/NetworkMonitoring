from email.mime.multipart import MIMEMultipart
import platform
import pytest, pyfakefs
from unittest.mock import patch, MagicMock
import os
import datetime
from monitorconnection import NetworkMonitor
from freezegun import freeze_time
import file_paths
import file_storage_configuration
from pingsettings import PingSettings
import datetime_functions
from pinger import get_pinger_class
from emailinfo import EmailInfo
import emailer

os.environ['ENV'] = 'test'
# mockPingSettings = PingSettings()
# mockPinger = get_pinger_class(mockPingSettings)
# mockNetworkMonitor = NetworkMonitor()

# storage_directories = file_paths.storage_directories
# log_storage_path = file_paths.log_storage_path
# log_file_name = file_paths.log_file_name

def test_build_email_message():
    test_message = emailer._build_email_message()
    assert test_message['From'] == EmailInfo.sender_email
    assert test_message['To'] == EmailInfo.receiver_email
    assert test_message['Subject'] == EmailInfo.subject_line
    assert test_message.get_payload()[0].get_payload() == EmailInfo.message_body
    
@freeze_time("2024-03-25")
def test_get_file_attachments():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    latency_chart_filename = f'{file_paths.latency_storage_path}/{current_date}-ping_latency_chart.png'
    success_chart_filename = f'{file_paths.success_storage_path}/{current_date}-ping_success_chart.png'
    
    attachments = emailer._get_file_attachments()
    
    assert len(attachments) == 3
    assert file_paths.log_file_name in attachments
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