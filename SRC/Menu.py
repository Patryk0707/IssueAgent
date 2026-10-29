import re
from pathlib import Path
from codeInput import codeInputToAgent
from sendEmail import send_status_email
from sendNotification import send_ntfy

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")

EMAIL_FILE = Path.home() / ".issueagent_email.txt"

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
        answer = input(f"Use saved email {savedEmail}? (Y/n) >>> ").strip().lower()
        if answer in ("", "y", "yes"):
            return savedEmail
    userEmail = input("Please enter your email (leave empty to skip) >>> ").strip()
    while userEmail and not isValidEmail(userEmail):
        userEmail = input("Invalid email. Try again (leave empty to skip) >>> ").strip()
    if userEmail:
        saveEmail(userEmail)
    return userEmail


def displayMenu():
    choice = "0"
    while choice !="4":
        choice=input("""
1.Enter code for the agent to check
2.Enter repository for agent to check for issues
3.Set agent to check repository for any issues
4.Finish session
>>> """)
        match choice:
            case "1":
                message = codeInputToAgent()
                print(message)

                # First line of the message is the subject, everything after is the body
                subject, _, body_text = message.strip().partition('\n')
                subject = subject.strip()
                body_text = body_text.strip()

                send_ntfy(subject, body_text)
                userEmail = getUserEmail()
                if userEmail:
                    send_status_email(userEmail, subject, body_text)
                else:
                    print("No email entered, email not sent.")

