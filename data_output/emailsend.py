import smtplib
from email.message import EmailMessage
import ssl
import getpass # To securely prompt for the password
import os
from dotenv import load_dotenv

load_dotenv()
sender_email = os.environ.get("SenderEmail")


def send_email(body, receiver_email):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = "ARB ALERT!"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    app_password = os.environ.get("TESTPASS")

    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        
        # Connect to the server and send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("Email sent successfully!")

    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
