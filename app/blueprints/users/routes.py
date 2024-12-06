import requests
from . import users_bp
from entities.user import UserEntity
from entities.user_log import UserLogEntity
from app.functions import get_verified_jwt_header
from app.decorators import RequirementsDecorators as restriction
from flask import render_template, redirect, url_for, flash, request, jsonify, session


@users_bp.route('/')
@restriction.login_required
@restriction.admin_required
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def users():
    try:
        response = requests.get(
            'http://localhost:8080/api/private/users/',
            headers=get_verified_jwt_header(),
            params={'user_idx': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status'):
                users_list = [
                    UserEntity(
                        user_id=user['user_id'],
                        user_username=user['user_username'],
                        user_email=user['user_email'],
                        user_name=user['user_name'],
                        user_lastname=user['user_lastname'],
                        user_privileges=user['user_privileges'],
                        user_state=user['user_state']
                    )
                    for user in response.json().get('users')
                ]
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to retrieve users')
        return render_template(
            'users/users.html',
            user_list=users_list,
            user=None
        )
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('users.users'))


@users_bp.route('/add', methods=['GET', 'POST'])
@restriction.login_required
@restriction.admin_required
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def add_user():
    if request.method == 'POST':
        try:
            response = requests.post(
                'http://localhost:8080/api/private/user/',
                headers=get_verified_jwt_header(),
                params={
                    'user_idx': session.get('user_id'),
                    'user_username': request.form['user_username'],
                    'user_email': request.form['user_email'],
                    'user_password': request.form['user_password'],
                    'user_name': request.form['user_name'],
                    'user_lastname': request.form['user_lastname'],
                    'user_privileges': request.form['user_privileges'],
                    'user_state': 1 if request.form['user_state'] == 'active' else 0
                }
            )
            if response.status_code == 200:
                if response.json().get('backend_status') == 200:
                    flash('User added successfully', 'success')
                    return redirect(url_for('users.users'))
                else:
                    raise Exception(response.json().get('message'))
            elif response.status_code == 500:
                raise Exception('Failed to add user')
        except Exception as e:
            flash(str(e), 'danger')
        return redirect(url_for('users.users'))

    try:
        return render_template(
            'users/form_users.html',
            user=None
        )
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('users.users'))


@users_bp.route('/update/<user_id>', methods=['GET', 'POST'])
@restriction.login_required
@restriction.admin_required
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def update_user(user_id):
    try:
        response = requests.get(
            f'http://localhost:8080/api/private/user/{user_id}',
            headers=get_verified_jwt_header(),
            params={'user_idx': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                user_obj = response.json().get('user')
                user = UserEntity(
                    user_id=user_obj['user_id'],
                    user_username=user_obj['user_username'],
                    user_email=user_obj['user_email'],
                    user_name=user_obj['user_name'],
                    user_lastname=user_obj['user_lastname'],
                    user_privileges=user_obj['user_privileges'],
                    user_state=user_obj['user_state']
                )
            else:
                flash(response.json().get('message'), 'danger')
                return redirect(url_for('users.users'))
        elif response.status_code == 500:
            flash('Failed to retrieve user', 'danger')
            return redirect(url_for('users.users'))
    except Exception as e:
        flash(str(e), 'danger')

    if request.method == 'POST':
        try:
            response = requests.put(
                f'http://localhost:8080/api/private/user/{user_id}',
                headers=get_verified_jwt_header(),
                params={
                    'user_idx': session.get('user_id'),
                    'user_id': user_id,
                    'user_username': request.form['user_username'],
                    'user_email': request.form['user_email'],
                    'user_password': request.form['user_password'],
                    'user_name': request.form['user_name'],
                    'user_lastname': request.form['user_lastname'],
                    'user_privileges': request.form['user_privileges'],
                    'user_state': (1 if request.form['user_state'] == 'active' else 0) if session.get(
                        'user_id') != user_id else 1
                }
            )
            if response.status_code == 200:
                if response.json().get('backend_status') == 200:
                    flash('User updated successfully', 'success')
                else:
                    raise Exception(response.json().get('message'))
            elif response.status_code == 500:
                raise Exception('Failed to update user')
        except Exception as e:
            flash(str(e), 'danger')
        return redirect(url_for('users.users'))

    try:
        return render_template(
            'users/form_users.html',
            user=user
        )
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('users.users'))


@users_bp.route('/delete/<int:user_id>', methods=['GET'])
@restriction.login_required
@restriction.admin_required
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def delete_user(user_id):
    try:
        response = requests.delete(
            f'http://localhost:8080/api/private/user/{user_id}',
            headers=get_verified_jwt_header(),
            params={'user_idx': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('User deleted successfully', 'success')
            else:
                flash(response.json().get('message'), 'danger')
        elif response.status_code == 500:
            flash('Failed to delete user', 'danger')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('users.users'))


@users_bp.route('/delete/bulk', methods=['POST'])
@restriction.login_required
@restriction.admin_required
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def bulk_delete_user():
    data = request.get_json()
    users_ids = data.get('items_ids', [])
    try:
        response = requests.delete(
            'http://localhost:8080/api/private/users/bulk/',
            headers=get_verified_jwt_header(),
            json={'users_ids': users_ids},
            params={'user_idx': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flag = response.json().get('count_flag')
                flash('Users deleted successfully', 'success')
                return jsonify({'message': f'{flag} Users deleted successfully'}), 200
            else:
                flash(response.json().get('message'), 'danger')
        elif response.status_code == 500:
            raise Exception('Failed to delete users')
    except Exception as e:
        flash(str(e), 'danger')
        return jsonify({'message': 'Failed to delete users', 'error': str(e)}), 500


@users_bp.route('/delete_all_users', methods=['POST'])
@restriction.login_required
@restriction.admin_required
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def delete_all_users():
    try:
        response = requests.delete(
            'http://localhost:8080/api/private/users/',
            headers=get_verified_jwt_header(),
            params={'user_idx': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('All Users deleted successfully', 'success')
                return jsonify({'message': 'All Users deleted successfully'}), 200
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to delete users')
    except Exception as e:
        flash(str(e), 'danger')
        return jsonify({'message': 'Failed to delete routers', 'error': str(e)}), 500


@users_bp.route('/log', methods=['GET'])
@restriction.login_required
@restriction.admin_required
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def log():
    try:
        response = requests.get(
            'http://localhost:8080/api/private/logs/',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                logs_list = [
                    UserLogEntity(
                        user_log_id=log['user_log_id'],
                        rk_user_id=log['rk_user_id'],
                        rk_user_username=log['rk_user_username'],
                        rk_user_name=log['rk_user_name'],
                        rk_user_lastname=log['rk_user_lastname'],
                        user_log_description=log['user_log_description'],
                        user_log_action=log['user_log_action'],
                        user_log_table=log['user_log_table'],
                        user_log_date=log['user_log_date'],
                        user_log_public_ip=log['user_log_public_ip'],
                        user_log_local_ip=log['user_log_local_ip']
                    )
                    for log in response.json().get('logs')
                ]
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to retrieve logs')
        return render_template(
            'users/log.html',
            user_log_list=logs_list
        )
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('users.log'))


@users_bp.route('/delete_from_date_user_log', methods=['POST'])
@restriction.login_required
@restriction.admin_required
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def delete_from_date_user_log():
    data = request.get_json()
    date = data.get('date', None)
    date += ' 23:59:59'
    try:
        response = requests.delete(
            'http://localhost:8080/api/private/logs/date/',
            headers=get_verified_jwt_header(),
            params={
                'date': date,
                'user_id': session.get('user_id')
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flag = response.json().get('flag')
                if flag == 0:
                    flash('No User Logs Found', 'danger')
                    return jsonify({'message': 'No User Logs Found'}), 200
                else:
                    flash(f'{flag} User Logs deleted successfully', 'success')
                    return jsonify({'message': 'User Logs deleted successfully'}), 200
            else:
                raise Exception(response.json().get('message'))
                return jsonify({'message': response.json().get('message')})
        elif response.status_code == 500:
            raise Exception('User Logs Failed to Delete')
            return jsonify({'message': 'User Logs Failed to Delete'})
    except Exception as e:
        flash(str(e), 'danger')
        return jsonify({'message': 'User Logs Failed to Delete', 'error': str(e)})
