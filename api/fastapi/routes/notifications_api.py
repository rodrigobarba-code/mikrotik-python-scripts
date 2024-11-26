from ...auth import verify_jwt
from fastapi import APIRouter, Depends, Request

from models.notifications.models import Notification

from ...functions import APIFunctions
from utils.threading_manager import ThreadingManager

notifications_router = APIRouter()
notifications_functions = APIFunctions()


@notifications_router.get('/notifications')
async def get_notifications(
        user_id: int,
        metadata: Request,
        token: dict = Depends(verify_jwt)
):
    try:
        if notifications_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(Notification.get_notifications, 'r', user_id)
            notifications = [
                {
                    'id': notification.notification_id,
                    'title': notification.notification_title,
                    'body': notification.notification_body,
                    'type': notification.notification_type,
                    'date': notification.notification_datetime,
                    'is_archived': notification.is_archived
                } for notification in request
            ]
            notifications_functions.create_transaction_log(
                action="GET",
                table="notifications",
                user_id=int(user_id),
                description="Notifications retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Notifications retrieved successfully",
                'notifications': notifications,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve notifications: {str(e)}",
            'backend_status': 400
        }
