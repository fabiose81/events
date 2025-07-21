import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from unittest.mock import patch, MagicMock

import constants
import email_sender

@patch.dict(os.environ, {
        "SENDER_EMAIL": "sender@email.com",
        "SENDER_EMAIL_PASSWORD": "password123",
        "SMTP_SERVER": "smtp.email.com",
        "SMTP_PORT": "587",
        "URI_VALIDATE_ACCOUNT": "http://api-service.com/activate?code=%c&email=%e"
    })
    
def test_send_email_success():
    receiver_email = "receiver@email.com"
    code = "687e540a5c694a229f935fe3"

    with patch("email_sender.smtplib.SMTP") as mock_smtp:

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = email_sender.send(receiver_email, code)

        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with(os.environ.get("SENDER_EMAIL"), os.environ.get("SENDER_EMAIL_PASSWORD"))
        mock_server.sendmail.assert_called_once()

        assert result == (constants.EMAIL_SENT, None)