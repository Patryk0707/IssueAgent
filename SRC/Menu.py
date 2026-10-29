from codeInput import codeInputToAgent
from sendEmail import send_status_email


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
            userEmail = input("Please enter your email >>>")
            send_status_email(userEmail, message)