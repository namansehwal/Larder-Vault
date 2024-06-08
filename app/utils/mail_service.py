import smtplib
import ssl
from email.message import EmailMessage

def send_email(email_receiver, subject, body):
    
    #credentials
    email_sender = 'thetorncondom@gmail.com'
    email_password = 'ojgo ugfy gkco oter'

    # Create the email message
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
    
    print('Mail Sent!!  to ', email_receiver, ' successfully')

# Example usage

email_receiver = 'namansehwal@gmail.com'
subject = 'Check out my new video!'
body = """
I've just published a new video on Aorus.
"""

send_email(email_receiver, subject, body)
