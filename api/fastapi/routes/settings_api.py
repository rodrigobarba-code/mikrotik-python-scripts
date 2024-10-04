# Importing necessary libraries and modules
from ...auth import verify_jwt
from fastapi import APIRouter, Depends, Request

from ...functions import APIFunctions
from entities.user import UserEntity
from models.users.models import User
from utils.threading_manager import ThreadingManager

settings_router = APIRouter()
settings_functions = APIFunctions()


@settings_router.put("/settings/user/{user_id}")
def update_settings_user(
        user_idx: int,
        metadata: Request,
        user_id: int,
        user_username: str,
        user_name: str,
        user_lastname: str,
):
    try:
        if settings_functions.verify_user_existence(user_idx):
            user = UserEntity(
                user_id=user_id,
                user_username=user_username,
                user_name=user_name,
                user_lastname=user_lastname
            )
            ThreadingManager().run_thread(User.update_settings_user, 'w', user)
            settings_functions.create_transaction_log(
                action="PUT",
                table="users",
                user_id=int(user_idx),
                description="Profile information updated successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Profile information updated successfully",
                'backend_status': 200,
                'new_username': user_username,
                'new_name': user_name,
                'new_lastname': user_lastname
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to update profile information: {str(e)}",
            'backend_status': 400
        }
