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
