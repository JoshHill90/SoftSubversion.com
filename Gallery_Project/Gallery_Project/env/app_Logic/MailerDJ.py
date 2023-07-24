import ssl
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
import os
from dotenv import load_dotenv

current_dir = Path(__file__).resolve().parent
ven = current_dir / ".env"
load_dotenv(ven)

print('stage-1')
#-------------------------------------------------------------------------------------------------------#
# Secret Values
#-------------------------------------------------------------------------------------------------------#


class AutoReply:

    email_host = os.getenv("EMAIL_HOSTING")
    send_from = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_port = os.getenv("EMAIL_PORT")
    email_backend = os.getenv("EMAIL_BACKEND_SMTP")
    alart_email = os.getenv("REPLYER")
    receive_email = os.getenv("RECEIVE_EMAILS")
    

    #------------------------#
    # Contact form auto reply
    #------------------------#

    def contact_request(self, reciver, name):

        contact_subject = "Thank You for Contacting Silk Thread Dev!"

        contact_body = f""" Dear {name}, """



        mailer = EmailMessage()

        mailer['From'] = formataddr(("Silk Thread Blog", f"{self.send_from}"))
        mailer['To'] = reciver
        mailer['Subject'] = contact_subject
        mailer.set_content(contact_body)

        with smtplib.SMTP(self.email_host, self.email_port) as server:
            try:
                server.starttls()
                server.login(self.send_from, self.email_password)
                server.sendmail(self.send_from, reciver, mailer.as_string())
                server.close()
                print('email sent')
            except Exception as e:
                print(f"An error occurred while sending the email: {e}")


    #------------------------#
    # Email Alart
    #------------------------#

    def contact_alart(self, email, name, subject, body):

        contact_subject = "Contact Form Alart"

        contact_body = f""" 
        Subject: {subject}

        From: {email} - Name: {name}

        Message:
            {body}"""



        mailer = EmailMessage()

        mailer['From'] = formataddr(("Contact Form", f"{self.alart_email}"))
        mailer['To'] = self.receive_email
        mailer['Subject'] = contact_subject
        mailer.set_content(contact_body)

        with smtplib.SMTP(self.email_host, self.email_port) as server:
            try:
                server.starttls()
                server.login(self.send_from, self.email_password)
                server.sendmail(self.send_from, self.receive_email, mailer.as_string())
                server.close()
                print('alart sent')
            except Exception as e:
                print(f"An error occurred while sending the email: {e}")


#### Test
"""test_send = os.getenv("TEST_SEND")

subject_test = "TEST"

body_test ="body"

SMTP = AutoReply()

SMTP.contact_request(test_send, 'john')
print('smtp request')
SMTP.contact_alart(test_send, 'john', subject_test, body_test)"""

