# Importing Required Libraries
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
def settings():
    return render_template('settings/settings.html', user_id=session.get('user_id'))


# Settings Main Route

# Update User Settings (Profile Information) Route with api
@settings_bp.route('/update', methods=['POST'])
@restriction.login_required
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
