import smtplib
from email.message import EmailMessage
import ssl
import getpass # To securely prompt for the password
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Debug: Check if .env file was found and loaded
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')

print(f"All env vars: {dict(os.environ)}")  # This will show all env vars


sender_email = os.environ.get("SenderEmail")
receiver_email = os.environ.get("RecipientEmail")
print(sender_email)

subject = "Email Sending with Python"
body = """
This is a test email sent using Python's smtplib library.
It demonstrates how to automate email sending in Python.
"""

# --- Create the email message ---
msg = EmailMessage()
msg.set_content(body)
msg['Subject'] = subject
msg['From'] = sender_email
msg['To'] = receiver_email

# --- Secure connection and login ---
# Get the App Password securely without displaying it
# You can also set it as an environment variable for better security
app_password = os.environ.get("TestPass")

print(app_password)
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
