import os
import smtplib
from email.mime.text import MIMEText

import constants

def send(receiver_email, code_activation):
    sender_email = os.environ.get("SENDER_EMAIL")
    password = os.environ.get("SENDER_EMAIL_PASSWORD")
    
    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_port = os.environ.get("SMTP_PORT") 

    body = constants.EMAIL_BODY
    body = body.replace("%uri", os.environ.get("URI_VALIDATE_ACCOUNT"))
    body = body.replace("%c", code_activation)
    body = body.replace("%e", receiver_email)
   
    message = MIMEText(body, "html")
    message["Subject"] = constants.EMAIL_SUBJECT
    message["From"] = sender_email
    message["To"] = receiver_email
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            return constants.EMAIL_SENT, None
    except Exception as e:
        return None, f"{constants.EMAIL_SEND_ERROR} : {e}"