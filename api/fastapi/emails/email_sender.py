import ssl
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.message import EmailMessage

class EmailSender:
    def __init__(self, sender_email, password, smtp_server='smtp.yandex.com', port=465):
        """
        Constructor for the EmailSender class.
        :param sender_email: Email address of the sender
        :param password: Password of the sender's email account
        :param smtp_server: SMTP server address (default is Gmail)
        :param port: Port number for the SMTP server (default is 465)
        """
        self.sender_email = sender_email
        self.password = password
        self.smtp_server = smtp_server
        self.port = port
        self.context = ssl.create_default_context()

    def _create_message(self, subject, body_html, recipients, attachment_path=None):
        """
        Create an email message with optional HTML body and attachment.
        """
        if not isinstance(recipients, list):
            recipients = [recipients]

        message = EmailMessage()
        message['From'] = self.sender_email
        message['To'] = ", ".join(recipients)
        message['Subject'] = subject
        message.add_alternative(body_html, subtype='html')

        if attachment_path:
            try:
                with open(attachment_path, 'rb') as attachment_file:
                    file_data = attachment_file.read()
                    file_name = attachment_file.name.split("/")[-1]
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(file_data)
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', f'attachment; filename="{file_name}"')
                message.attach(attachment)
            except FileNotFoundError:
                print(f"Attachment file '{attachment_path}' not found. Skipping attachment.")

        return message

    def send_email(self, subject, body_html, recipients, attachment_path=None):
        """
        Send an email to one or multiple recipients with optional attachment.
        """
        message = self._create_message(subject, body_html, recipients, attachment_path)

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=self.context) as smtp:
                smtp.login(self.sender_email, self.password)
                smtp.sendmail(self.sender_email, recipients, message.as_string())
                print(f"Email successfully sent to {', '.join(recipients)}.")
        except smtplib.SMTPException as e:
            print(f"Failed to send email: {e}")

    @staticmethod
    def read_html_template(file_path, metadata: dict):
        """
        Read an HTML file, replace placeholders like {{ key }} with values from metadata, and return the content as a string.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Replace placeholders {{ key }} with corresponding values from metadata
            for key, value in metadata.items():
                placeholder = f"{{{{ {key} }}}}"  # This creates the placeholder format {{ key }}
                html_content = html_content.replace(placeholder, str(value))

            return html_content
        except FileNotFoundError as e:
            print(f"HTML file '{file_path}' not found.")
            raise e
