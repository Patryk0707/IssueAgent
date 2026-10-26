from codeInput import codeInputToAgent
import sendEmail


def displayMenu():
    choice=input("""
    1.Enter code for the agent to check
    2.Enter repository for agent to check for issues
    3.Set agent to check repository for any issues
    """)
    match choice:
        case "1":
            message = codeInputToAgent()
            print(message)
            userEmail = input("Please enter your email >>>")
            sendEmail.send_status_email(userEmail, 'subject', message)