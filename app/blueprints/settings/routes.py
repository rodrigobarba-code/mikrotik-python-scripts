# Importing Required Libraries
from tempfile import template

import requests
from . import settings_bp
from entities.user import UserEntity
from entities.user_log import UserLogEntity
from app.functions import get_verified_jwt_header
from app.decorators import RequirementsDecorators as restriction
from flask import render_template, redirect, url_for, flash, request, jsonify, session


# Importing Required Libraries

# Setiings Main Route
@settings_bp.route('/', methods=['GET'])
@restriction.login_required
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def settings():
    return render_template('settings/settings.html', user_id=session.get('user_id'))


# Settings Main Route

# Update User Settings (Profile Information) Route with api
@settings_bp.route('/update', methods=['POST'])
@restriction.login_required
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def update_settings():
    if request.method == 'POST':
        try:
            response = requests.put(
                f'http://localhost:8080/api/private/settings/user/{session.get("user_id")}',
                headers=get_verified_jwt_header(),
                params={
                    'user_idx': session.get('user_id'),
                    'user_id': session.get('user_id'),
                    'user_username': request.form['user_username'],
                    'user_name': request.form['user_name'],
                    'user_lastname': request.form['user_lastname']
                }
            )
            if response.status_code == 200:
                if response.json().get('backend_status') == 200:
                    session['user_username'] = response.json().get('new_username')
                    session['user_name'] = response.json().get('new_name')
                    session['user_lastname'] = response.json().get('new_lastname')
                    flash('User updated successfully', 'success')
                else:
                    raise Exception(response.json().get('message'))
            elif response.status_code == 500:
                raise Exception('Failed to update user')
        except Exception as e:
            flash(str(e), 'danger')
        return redirect(url_for('settings.settings'))

    try:
        return render_template(
            'settings/settings.html',
        )
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('settings.settings'))


# Update User Settings (Profile Information) Route with api

# Change user password Route with api
@settings_bp.route('/update-password', methods=['POST'])
@restriction.login_required
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def update_password():
    if request.method == 'POST':
        try:
            response = requests.put(
                f'http://localhost:8080/api/private/settings/user/password/{session.get("user_id")}',
                headers=get_verified_jwt_header(),
                params={
                    'user_idx': session.get('user_id'),
                    'user_id': session.get('user_id'),
                    'user_username': session.get('user_username'),
                    'user_password': request.form['old_password'],
                    'new_password': request.form['new_password'],
                }
            )
            if response.status_code == 200:
                if response.json().get('backend_status') == 200:
                    session['user_password'] = response.json().get('new_password')
                    flash('Password updated successfully', 'success')
                else:
                    raise Exception(response.json().get('message'))
            elif response.status_code == 500:
                raise Exception('Failed to update password')
        except Exception as e:
            flash(str(e), 'danger')
        return redirect(url_for('settings.settings'))

    try:
        return render_template(
            'settings/settings.html',
        )
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('settings.settings'))


# Change user password Route with api

# Account Deletion Route with api but check password before deletion
@settings_bp.route('/delete', methods=['POST'])
@restriction.login_required
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def delete_account():
    import time
    is_deleted = False
    try:
        response = requests.delete(
            f'http://localhost:8080/api/private/settings/user/delete/',
            headers=get_verified_jwt_header(),
            params={
                'user_idx': session.get('user_id'),
                'user_username': session.get('user_username'),
                'user_password': request.form['user_password']
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                is_deleted = True
                flash('Account deleted successfully', 'success')
            else:
                flash(response.json().get('message'), 'danger')
                return redirect(url_for('settings.settings'))
        elif response.status_code == 500:
            flash('Failed to delete the account', 'danger')
            return redirect(url_for('settings.settings'))
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('settings.settings'))
    finally:
        if is_deleted:
            return render_template('auth/login.html')
# Account Deletion Route with api
