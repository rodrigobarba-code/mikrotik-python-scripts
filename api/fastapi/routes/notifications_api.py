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


@notifications_router.get('/notifications/unarchived')
async def get_unarchived_notifications(
        user_id: int,
        metadata: Request,
        token: dict = Depends(verify_jwt)
):
    try:
        if notifications_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(Notification.get_unarchived_notifications, 'r', user_id)
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
                description="Unarchived notifications retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Unarchived notifications retrieved successfully",
                'notifications': notifications,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve unarchived notifications: {str(e)}",
            'backend_status': 400
        }


@notifications_router.get('/notifications/archived')
async def get_archived_notifications(
        user_id: int,
        metadata: Request,
        token: dict = Depends(verify_jwt)
):
    try:
        if notifications_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(Notification.get_archived_notifications, 'r', user_id)
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
                description="Archived notifications retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Archived notifications retrieved successfully",
                'notifications': notifications,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve archived notifications: {str(e)}",
            'backend_status': 400
        }


@notifications_router.put('/notification/{notification_id}')
async def archive_notification(
        notification_id: int,
        user_id: int,
        metadata: Request,
        token: dict = Depends(verify_jwt)
):
    try:
        if notifications_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(Notification.archive_notification, 'w', notification_id)
            notifications_functions.create_transaction_log(
                action="PUT",
                table="notifications",
                user_id=int(user_id),
                description="Notification archived successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Notification archived successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to archive notification: {str(e)}",
            'backend_status': 400
        }


@notifications_router.put('/notification/{notification_id}/restore')
async def restore_notification(
        notification_id: int,
        user_id: int,
        metadata: Request,
        token: dict = Depends(verify_jwt)
):
    try:
        if notifications_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(Notification.unarchive_notification, 'w', notification_id)
            notifications_functions.create_transaction_log(
                action="PUT",
                table="notifications",
                user_id=int(user_id),
                description="Notification unarchived successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Notification unarchived successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to unarchive notification: {str(e)}",
            'backend_status': 400
        }


@notifications_router.delete('/notification/{notification_id}')
async def delete_notification(
        notification_id: int,
        user_id: int,
        metadata: Request,
        token: dict = Depends(verify_jwt)
):
    try:
        if notifications_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(Notification.delete_notification, 'w', notification_id)
            notifications_functions.create_transaction_log(
                action="DELETE",
                table="notifications",
                user_id=int(user_id),
                description="Notification deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Notification deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete notification: {str(e)}",
            'backend_status': 400
        }


@notifications_router.get('/notifications/unread')
async def get_unread_notifications(
        token: dict = Depends(verify_jwt)
):
    try:
        if True:
            request = ThreadingManager().run_thread(Notification.get_notifications, 'r')
            temp = [
                i for i in request if i.is_archived == 0
            ]
            count = len(temp)
            return {
                'message': "Unread notifications retrieved successfully",
                'count': count,
                'backend_status': 200
            }
    except Exception as e:
        return {
            'message': f"Failed to retrieve unread notifications: {str(e)}",
            'backend_status': 400
        }
