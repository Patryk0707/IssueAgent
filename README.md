# IssueAgent

This project is developed to help programmers check their programs for errors, tell them what it is and help fix it. It can check a single piece of code and a GitHub repository.


### Send email

The agent is given an instruction to make the first line of his response a subject for the email. Everything after the first line will be the body of the email. The program lets user send the email or don't do anything. The program validates the email address. The program saves the last entered email address locally, allowing to reuse it in the future

To send an email, you need to set up SENDER_EMAIL APP_PASSWORD locally. 


### Send notification

Notifications are sent via ntfy. They use the same principle as send email. You need to make your own topic in ntfy to be able to receive emails.

To send a notification, you need to set up NTFY_SERVER NTFY_TOPIC locally. 


### Requirements

#### Libraries

In order for the project to work, you need to download those libraries using ```pip install ...```

Flask
gunicorn
openai
gitingest
loguru

#### Environmental variables

To run the project, you need to set up those variables locally:

NEBIUS_API_KEY
SENDER_EMAIL
APP_PASSWORD
NTFY_TOPIC