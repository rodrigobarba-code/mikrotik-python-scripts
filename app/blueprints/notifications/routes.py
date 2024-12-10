# Importing Required Libraries
import requests
from . import notifications_bp
from app.functions import get_verified_jwt_header
from entities.notification import NotificationEntity
from flask import render_template, flash, jsonify, session
from app.decorators import RequirementsDecorators as restriction


# Get unarchived notifications
def get_unarchived_notifications() -> list:
    """
    Get notifications from the API
    :return: list
    """
    try:
        response = requests.get(
            'http://localhost:8080/api/private/notifications/unarchived/',
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


# Get archived notifications
def get_archived_notifications() -> list:
    """
    Get notifications from the API
    :return: list
    """
    try:
        response = requests.get(
            'http://localhost:8080/api/private/notifications/archived/',
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
        notification_list=get_unarchived_notifications(),
        archived=False
    )


@notifications_bp.route('/archived', methods=['GET'])
@restriction.login_required  # Login Required Decorator
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def archived_notifications():
    return render_template(
        'notifications/notifications.html',
        notification_list=get_archived_notifications(),
        archived=True
    )


@notifications_bp.route('/archive/<int:notification_id>', methods=['POST'])
@restriction.login_required  # Login Required Decorator
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def archive_notification(notification_id: int):
    try:
        response = requests.put(
            f'http://localhost:8080/api/private/notification/{notification_id}',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('Notification archived successfully', 'success')
                return jsonify({'status': 'success'}), 200
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to archive notification')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return jsonify({'status': str(e)}), 500


@notifications_bp.route('/restore/<int:notification_id>', methods=['POST'])
@restriction.login_required  # Login Required Decorator
@restriction.redirect_to_loading_screen  # Redirect to Loading
def restore_notification(notification_id: int):
    try:
        response = requests.put(
            f'http://localhost:8080/api/private/notification/{notification_id}/restore/',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('Notification unarchived successfully', 'success')
                return jsonify({'status': 'success'}), 200
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to unarchive notification')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return jsonify({'status': str(e)}), 500


@notifications_bp.route('/delete/<int:notification_id>', methods=['POST'])
@restriction.login_required  # Login Required Decorator
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def delete_notification(notification_id: int):
    try:
        response = requests.delete(
            f'http://localhost:8080/api/private/notification/{notification_id}',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('Notification deleted successfully', 'success')
                return jsonify({'status': 'success'}), 200
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to delete notification')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return jsonify({'status': str(e)}), 500


@notifications_bp.route('/archive/all', methods=['POST'])
@restriction.login_required  # Login Required Decorator
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def archive_all_notifications():
    try:
        response = requests.put(
            'http://localhost:8080/api/private/notifications/',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('Notifications archived successfully', 'success')
                return jsonify({'status': 'success'}), 200
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to archive notifications')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return jsonify({'status': str(e)}), 500


@notifications_bp.route('/restore/all', methods=['POST'])
@restriction.login_required  # Login Required Decorator
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def restore_all_notifications():
    try:
        response = requests.put(
            'http://localhost:8080/api/private/notifications/restore/',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('Notifications restored successfully', 'success')
                return jsonify({'status': 'success'}), 200
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to restore notifications')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return jsonify({'status': str(e)}), 500


@notifications_bp.route('/delete/all', methods=['POST'])
@restriction.login_required  # Login Required Decorator
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def delete_all_notifications():
    try:
        response = requests.delete(
            'http://localhost:8080/api/private/notifications/',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('Notifications deleted successfully', 'success')
                return jsonify({'status': 'success'}), 200
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to delete notifications')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return jsonify({'status': str(e)}), 500
