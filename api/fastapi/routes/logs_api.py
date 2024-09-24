from ..auth import verify_jwt
from fastapi import APIRouter, Depends, Request
from utils.threading_manager import ThreadingManager

from..functions import APIFunctions
from models.users.models import UserLog

logs_router = APIRouter()
logs_functions = APIFunctions()

@logs_router.get("/logs/")
async def get_logs(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if logs_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(UserLog.get_user_logs, 'r')
            user_logs = [
                {
                    "user_log_id": log.user_log_id,
                    "rk_user_id": log.rk_user_id,
                    "rk_user_username": log.rk_user_username,
                    "rk_user_name": log.rk_user_name,
                    "rk_user_lastname": log.rk_user_lastname,
                    "user_log_description": log.user_log_description,
                    "user_log_action": log.user_log_action,
                    "user_log_table": log.user_log_table,
                    "user_log_date": log.user_log_date,
                    "user_log_public_ip": log.user_log_public_ip,
                    "user_log_local_ip": log.user_log_local_ip
                }
                for log in request
            ]
            logs_functions.create_transaction_log(
                action="GET",
                table="logs",
                user_id=int(user_id),
                description="User logs retrieved",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Logs retrieved successfully",
                'logs': user_logs,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve logs: {str(e)}",
            'backend_status': 400
        }

@logs_router.delete("/logs/date/")
async def delete_logs_by_date(user_id: int, metadata: Request, date: str, token: dict = Depends(verify_jwt)):
    try:
        if logs_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(UserLog.delete_from_date_user_log, 'w', date)
            logs_functions.create_transaction_log(
                action="DELETE",
                table="logs",
                user_id=int(user_id),
                description=f"Logs deleted by date: {date}",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Logs deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete logs: {str(e)}",
            'backend_status': 400
        }

@logs_router.delete("/logs/")
async def delete_logs(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if logs_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(UserLog.delete_all_user_log, 'wx')
            logs_functions.create_transaction_log(
                action="DELETE",
                table="logs",
                user_id=int(user_id),
                description="All logs deleted",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Logs deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete logs: {str(e)}",
            'backend_status': 400
        }
