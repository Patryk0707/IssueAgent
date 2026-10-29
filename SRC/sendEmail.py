import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# Set up email configuration
import os
sender_email = os.environ["SENDER_EMAIL"]
app_password = os.environ["APP_PASSWORD"]

def send_status_email(receiver_email, subject, body_text):
    # Structure the message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = Header(subject, 'utf-8')
    msg.attach(MIMEText(body_text, 'plain', 'utf-8'))

    # Connect to server and send
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

    return 0