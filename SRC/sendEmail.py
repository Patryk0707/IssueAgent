import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_status_email(receiver_email, subject, body_text):
    # 1. Setup email configuration
    sender_email = "issueagent007@gmail.com"
    app_password = "**** **** **** ****"  # Generated 16-character App Password
    
    # 2. Structure the message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body_text, 'plain'))
    
    # 3. Connect to server and send
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

    return 0




