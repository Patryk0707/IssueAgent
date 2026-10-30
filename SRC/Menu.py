from codeInput import codeInputToAgent
import sendEmail
import sendNotification
import checkRepo
from scanRepo import listen


def displayMenu():
    choice = "0"
    while choice !="4":
        choice=input("""
1.Enter code for the agent to check
2.Enter repository for agent to check for issues
3.Set agent to check repository for any issues
4.Finish session
>>>""")
        match choice:
            case "1":
                message = codeInputToAgent()
                print(message)
                subject, _, body_text = message.strip().partition('\n')
                subject = subject.strip()
                body_text = body_text.strip()
                sendNotification.send_ntfy(subject, body_text)
                userEmail = sendEmail.getUserEmail()
                if userEmail:
                    # First line of the message is the subject, everything after is the body
                    sendEmail.send_status_email(userEmail, subject, body_text)
                else:
                    print("No email entered, email not sent.")

            case "2":
                userRepo=input("Enter Repository for agent to check for issues: ")
                message = checkRepo.checkRepoByCode(userRepo)
                print(message)

            case "3":
                listen()

            case "4":
                exit()