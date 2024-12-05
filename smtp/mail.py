import ssl
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.message import EmailMessage

# Define email sender and receiver
email_sender = 'sevensuite.service.noreply@gmail.com'
email_password = 'rodj eotq jgci lktn '
email_receiver = ''

# Set the subject and body of the email
subject = 'Seven Suite Test Email'
body = " <h1> This is a test email from Seven Suite </h1>"

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

# Make the message multipart
em.add_alternative(body, subtype='html')

# Attach the image file
with open('image.jpg', 'rb') as attachment_file:
    file_data = attachment_file.read()
    file_name = attachment_file.name.split("/")[-1]

attachment = MIMEBase('application', 'octet-stream')
attachment.set_payload(file_data)
encoders.encode_base64(attachment)
attachment.add_header('Content-Disposition', f'attachment; filename="{file_name}"')
em.attach(attachment)

# Add SSL (layer of security)
context = ssl.create_default_context()

# Log in and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
