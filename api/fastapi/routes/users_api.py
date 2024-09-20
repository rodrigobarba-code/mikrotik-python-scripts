from typing import List
from ..auth import verify_jwt
from pydantic import BaseModel
from fastapi import APIRouter, Depends

from entities.user import UserEntity
from models.users.models import User
from utils.threading_manager import ThreadingManager

users_router = APIRouter()

class UserBulkDeleteBase(BaseModel):
    users_ids: List[int]

@users_router.get("/users/")
async def get_users(token: dict = Depends(verify_jwt)):
    try:
        request = ThreadingManager().run_thread(User.get_users, 'r')
        user_list = [
            {
                "user_id": user.user_id,
                "user_username": user.user_username,
                "user_password": user.user_password,
                "user_name": user.user_name,
                "user_lastname": user.user_lastname,
                "user_privileges": user.user_privileges,
                "user_state": user.user_state
            }
            for user in request
        ]
        return {
            'message': "Users retrieved successfully",
            'users': user_list,
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to retrieve users: {str(e)}",
            'backend_status': 400
        }

@users_router.get("/user/{user_id}")
def get_user(user_id: int, token: dict = Depends(verify_jwt)):
    try:
        request = ThreadingManager().run_thread(User.get_user, 'rx', user_id)
        return {
            'message': "User retrieved successfully",
            'user': {
                "user_id": request.user_id,
                "user_username": request.user_username,
                "user_password": request.user_password,
                "user_name": request.user_name,
                "user_lastname": request.user_lastname,
                "user_privileges": request.user_privileges,
                "user_state": request.user_state
            },
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to retrieve user: {str(e)}",
            'backend_status': 400
        }

@users_router.post("/user/")
def add_user(
    user_username: str,
    user_password: str,
    user_name: str,
    user_lastname: str,
    user_privileges: str,
    user_state: int,
    token: dict = Depends(verify_jwt)
):
    try:
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
        return {
            'message': "User updated successfully",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to update user: {str(e)}",
            'backend_status': 400
        }

@users_router.delete("/user/{user_id}")
def delete_user(user_id: int, token: dict = Depends(verify_jwt)):
    try:
        ThreadingManager().run_thread(User.delete_user, 'w', user_id)
        return {
            'message': "User deleted successfully",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to delete user: {str(e)}",
            'backend_status': 400
        }

@users_router.delete("/users/bulk/")
def bulk_delete_users(request: UserBulkDeleteBase, token: dict = Depends(verify_jwt)):
    try:
        ThreadingManager().run_thread(User.bulk_delete_users, 'w', request.users_ids)
        return {
            'message': "Bulk delete users successful",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to bulk delete users: {str(e)}",
            'backend_status': 400
        }

@users_router.delete("/users/")
def delete_users(token: dict = Depends(verify_jwt)):
    try:
        ThreadingManager().run_thread(User.delete_users, 'w')
        return {
            'message': "Delete users successful",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to delete users: {str(e)}",
            'backend_status': 400
        }
