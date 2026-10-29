import re
from codeInput import codeInputToAgent
from sendEmail import send_status_email

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")

def isValidEmail(email):
    return bool(EMAIL_PATTERN.match(email))


def displayMenu():
    choice=input("""
1.Enter code for the agent to check
2.Enter repository for agent to check for issues
3.Set agent to check repository for any issues
>>>""")
    match choice:
        case "1":
            message = codeInputToAgent()
            print(message)
            userEmail = input("Please enter your email (leave empty to skip) >>>").strip()
            while userEmail and not isValidEmail(userEmail):
                userEmail = input("Invalid email. Try again (leave empty to skip) >>>").strip()
            if userEmail:
                send_status_email(userEmail, message)
            else:
                print("No email entered, email not sent.")