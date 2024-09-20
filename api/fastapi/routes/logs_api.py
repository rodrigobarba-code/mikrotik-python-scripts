from ..auth import verify_jwt
from fastapi import APIRouter, Depends
from utils.threading_manager import ThreadingManager

from models.users.models import UserLog

logs_router = APIRouter()

@logs_router.get("/logs/")
async def get_logs(token: dict = Depends(verify_jwt)):
    try:
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
        return {
            'message': "Logs retrieved successfully",
            'logs': user_logs,
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to retrieve logs: {str(e)}",
            'backend_status': 400
        }

@logs_router.delete("/logs/date/")
async def delete_logs_by_date(date: str, token: dict = Depends(verify_jwt)):
    try:
        ThreadingManager().run_thread(UserLog.delete_user_log_by_date, 'w', date)
        return {
            'message': "Logs deleted successfully",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to delete logs: {str(e)}",
            'backend_status': 400
        }

@logs_router.delete("/logs/")
async def delete_logs(token: dict = Depends(verify_jwt)):
    try:
        ThreadingManager().run_thread(UserLog.delete_all_user_log, 'w')
        return {
            'message': "Logs deleted successfully",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to delete logs: {str(e)}",
            'backend_status': 400
        }
