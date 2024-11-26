# Importing Required Libraries
import requests
from . import notifications_bp
from entities.notification import NotificationEntity
from app.functions import get_verified_jwt_header
from app.decorators import RequirementsDecorators as restriction
from flask import render_template, redirect, url_for, flash, request, jsonify, session

# Get notifications
def get_notifications() -> list:
    """
    Get notifications from the API
    :return: list
    """
    try:
        response = requests.get(
            'http://localhost:8080/api/private/notifications/',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                return [
                    NotificationEntity(
                        notification_id=notification.get('id'),
                        notification_title=notification.get('title'),
                        notification_body=notification.get('body'),
                        notification_type=notification.get('type'),
                        notification_datetime=notification.get('date'),
                        is_archived=notification.get('is_archived')
                    ) for notification in response.json().get('notifications')
                ]
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to retrieve regions')
    except Exception as e:
        print(f'Error: {str(e)}')
        return []

# Dashboard Main Route
@notifications_bp.route('/', methods=['GET'])
@restriction.login_required  # Login Required Decorator
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def notifications():
    return render_template(
        'notifications/notifications.html',
        notification_list=get_notifications()
    )
