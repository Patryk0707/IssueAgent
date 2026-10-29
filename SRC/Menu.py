from codeInput import codeInputToAgent
import sendEmail
import sendNotification


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

                # First line of the message is the subject, everything after is the body
                subject, _, body_text = message.strip().partition('\n')
                subject = subject.strip()
                body_text = body_text.strip()

                sendNotification.send_ntfy(subject, body_text)

                userEmail = sendEmail.getUserEmail()
                if userEmail:
                    sendEmail.send_status_email(userEmail, subject, body_text)
                else:
                    print("No email entered, email not sent.")