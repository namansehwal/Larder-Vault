import smtplib
import ssl
from email.message import EmailMessage

# Define email sender and receiver
email_sender = 'thetorncondom@gmail.com'
email_password = 'ojgo ugfy gkco oter'
email_receiver = 'namansehwal@gmail.com'

# Set the subject and body of the email
subject = 'Check out my new video!'
body = """
I've just published a new video on Aorus.
"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

# Add SSL (layer of security)
context = ssl.create_default_context()

# Log in and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())

print('Mail Sent!!')    