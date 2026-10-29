from codeInput import codeInputToAgent
import sendEmail



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
            userEmail = sendEmail.getUserEmail()
            if userEmail:
                sendEmail.send_status_email(userEmail, message)
            else:
                print("No email entered, email not sent.")