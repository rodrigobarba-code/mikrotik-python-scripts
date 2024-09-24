from typing import List
from ..auth import verify_jwt
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request

from ..functions import APIFunctions
from entities.user import UserEntity
from models.users.models import User
from utils.threading_manager import ThreadingManager

users_router = APIRouter()
users_functions = APIFunctions()

class UserBulkDeleteBase(BaseModel):
    users_ids: List[int]

@users_router.get("/users/")
async def get_users(user_idx: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if users_functions.verify_user_existence(user_idx):
            request = ThreadingManager().run_thread(User.get_users, 'r')
            user_list = [
                {
                    "user_id": user.user_id,
                    "user_username": user.user_username,
                    "user_name": user.user_name,
                    "user_lastname": user.user_lastname,
                    "user_privileges": user.user_privileges,
                    "user_state": user.user_state
                }
                for user in request
            ]
            users_functions.create_transaction_log(
                action="GET",
                table="users",
                user_id=int(user_idx),
                description="Users retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Users retrieved successfully",
                'users': user_list,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve users: {str(e)}",
            'backend_status': 400
        }

@users_router.get("/user/{user_id}")
def get_user(user_idx: int, metadata: Request, user_id: int, token: dict = Depends(verify_jwt)):
    try:
        if users_functions.verify_user_existence(user_idx):
            request = ThreadingManager().run_thread(User.get_user, 'rx', user_id)
            user = {
                "user_id": request.user_id,
                "user_username": request.user_username,
                "user_name": request.user_name,
                "user_lastname": request.user_lastname,
                "user_privileges": request.user_privileges,
                "user_state": request.user_state
            }
            users_functions.create_transaction_log(
                action="GET",
                table="users",
                user_id=int(user_idx),
                description="User retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "User retrieved successfully",
                'user': user,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve user: {str(e)}",
            'backend_status': 400
        }

@users_router.post("/user/")
def add_user(
    user_idx: int,
    metadata: Request,
    user_username: str,
    user_password: str,
    user_name: str,
    user_lastname: str,
    user_privileges: str,
    user_state: int,
    token: dict = Depends(verify_jwt)
):
    try:
        if users_functions.verify_user_existence(user_idx):
            user = UserEntity(
                user_id=int(),
                user_username=user_username,
                user_password=user_password,
                user_name=user_name,
                user_lastname=user_lastname,
                user_privileges=user_privileges,
                user_state=user_state
            )
            ThreadingManager().run_thread(User.add_user, 'w', user)
            users_functions.create_transaction_log(
                action="POST",
                table="users",
                user_id=int(user_idx),
                description="User added successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "User added successfully",
                'backend_status': 200
            }
    except Exception as e:
        return {
            'message': f"Failed to add user: {str(e)}",
            'backend_status': 400
        }

@users_router.put("/user/{user_id}")
def update_user(
    user_idx: int,
    metadata: Request,
    user_id: int,
    user_username: str,
    user_password: str,
    user_name: str,
    user_lastname: str,
    user_privileges: str,
    user_state: int,
    token: dict = Depends(verify_jwt)
):
    try:
        if users_functions.verify_user_existence(user_idx):
            user = UserEntity(
                user_id=user_id,
                user_username=user_username,
                user_password=user_password,
                user_name=user_name,
                user_lastname=user_lastname,
                user_privileges=user_privileges,
                user_state=user_state
            )
            ThreadingManager().run_thread(User.update_user, 'w', user)
            users_functions.create_transaction_log(
                action="PUT",
                table="users",
                user_id=int(user_idx),
                description="User updated successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "User updated successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to update user: {str(e)}",
            'backend_status': 400
        }

@users_router.delete("/user/{user_id}")
def delete_user(user_idx: int, metadata: Request, user_id: int, token: dict = Depends(verify_jwt)):
    try:
        if users_functions.verify_user_existence(user_idx):
            ThreadingManager().run_thread(User.delete_user, 'w', user_id)
            users_functions.create_transaction_log(
                action="DELETE",
                table="users",
                user_id=int(user_idx),
                description="User deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "User deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete user: {str(e)}",
            'backend_status': 400
        }

@users_router.delete("/users/bulk/")
def bulk_delete_users(user_idx: int, metadata: Request, request: UserBulkDeleteBase, token: dict = Depends(verify_jwt)):
    try:
        if users_functions.verify_user_existence(user_idx):
            ThreadingManager().run_thread(User.bulk_delete_users, 'w', request.users_ids)
            users_functions.create_transaction_log(
                action="DELETE",
                table="users",
                user_id=int(user_idx),
                description="Users deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Users deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to bulk delete users: {str(e)}",
            'backend_status': 400
        }

@users_router.delete("/users/")
def delete_users(user_idx: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if users_functions.verify_user_existence(user_idx):
            ThreadingManager().run_thread(User.delete_users, 'wx')
            users_functions.create_transaction_log(
                action="DELETE",
                table="users",
                user_id=int(user_idx),
                description="Users deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Users deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete users: {str(e)}",
            'backend_status': 400
        }
