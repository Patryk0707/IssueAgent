import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import re
from pathlib import Path

# Set up email configuration
import os
sender_email = "issueagent007@gmail.com"
app_password = os.environ.get("APP_PASSWORD")

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")
EMAIL_FILE = Path.home() / ".issueagent_email.txt"

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
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def isValidEmail(email):
    return bool(EMAIL_PATTERN.match(email))


def loadSavedEmail():
    try:
        email = EMAIL_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        return ""
    return email if isValidEmail(email) else ""


def saveEmail(email):
    try:
        EMAIL_FILE.write_text(email, encoding="utf-8")
    except OSError as e:
        print(f"Could not save email: {e}")


def getUserEmail():
    savedEmail = loadSavedEmail()
    if savedEmail:
        answer = input(f"Use saved email {savedEmail}? (Y/n) >>>").strip().lower()
        if answer in ("", "y", "yes"):
            return savedEmail
    userEmail = input("Please enter your email (leave empty to skip) >>>").strip()
    while userEmail and not isValidEmail(userEmail):
        userEmail = input("Invalid email. Try again (leave empty to skip) >>>").strip()
    if userEmail:
        saveEmail(userEmail)
    return userEmail
