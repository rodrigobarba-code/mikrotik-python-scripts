import os
from ...auth import verify_jwt
from fastapi import APIRouter, Depends

from dotenv import load_dotenv
from models.users.models import User
from ...functions import APIFunctions
from ..emails.email_sender import EmailSender
from utils.threading_manager import ThreadingManager

emailsender_router = APIRouter()
emailsender_functions = APIFunctions()

load_dotenv()

@emailsender_router.get("/email/reset-password/")
async def reset_password_email(
        user_email: str,
        token: dict = Depends(verify_jwt)
):
    try:
        # Reset the user's password with a random one
        data = ThreadingManager().run_thread(
            User.reset_password_with_random,
            'rxc',
            user_email
        )

        # Initialize the email sender
        email_sender = EmailSender(
            sender_email=os.getenv('SENDER_EMAIL'),
            password=os.getenv('SENDER_PASSWORD'),
        )

        # Define email details
        subject = 'Reset Your Password - Seven Suite'
        html_file_path = 'api/fastapi/emails/templates/forgot_password.html'
        html_content = email_sender.read_html_template(html_file_path, data)
        recipients = [user_email]

        # Send email
        email_sender.send_email(
            subject=subject,
            body_html=html_content,
            recipients=recipients,
            attachment_path=None
        )

        return {
            'message': "Password reset email sent successfully.",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to send password reset email: {e}",
            'backend_status': 400
        }

@emailsender_router.get("/email/welcome/")
async def welcome_email(
        user_username: str,
        user_password: str,
        token: dict = Depends(verify_jwt)
):
    try:
        # Get the user's data
        data = ThreadingManager().run_thread(
            User.get_user_by_username,
            'rx',
            user_username
        )

        if data is None:
            raise Exception("User not found.")

        # Create user metadata
        user_metadata = {
            'user_name': data.user_name,
            'user_lastname': data.user_lastname,
            'user_username': data.user_username,
            'user_password': user_password,
        }

        # Initialize the email sender
        email_sender = EmailSender(
            sender_email=os.getenv('SENDER_EMAIL'),
            password=os.getenv('SENDER_PASSWORD'),
        )

        # Define email details
        subject = 'Welcome to Seven Suite'
        html_file_path = 'api/fastapi/emails/templates/welcome.html'
        html_content = email_sender.read_html_template(html_file_path, user_metadata)
        recipients = [data.user_email]

        # Send email
        email_sender.send_email(
            subject=subject,
            body_html=html_content,
            recipients=recipients,
            attachment_path=None
        )

        return {
            'message': "Welcome email sent successfully.",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to send welcome email: {e}",
            'backend_status': 400
        }
