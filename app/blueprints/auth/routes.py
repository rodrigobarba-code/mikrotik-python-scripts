import os
import requests
from . import auth_bp
from datetime import timedelta
from dotenv import load_dotenv
from app.functions import get_verified_jwt_header
from app.functions import get_local_ip, get_public_ip
from app.decorators import RequirementsDecorators as restrictions
from flask import render_template, redirect, url_for, flash, request, session, current_app, jsonify

load_dotenv()


@auth_bp.route('/login', methods=['GET', 'POST'])
async def login():
    session.clear()
    dev_mode = os.getenv('DEVELOPMENT_MODE', 'True').lower() in ['true', '1', 't']

    if dev_mode:
        session['user_id'] = os.getenv('SUPER_ADMIN_ID')
        session['user_username'] = os.getenv('SUPER_ADMIN_USER')
        session['user_privileges'] = os.getenv('SUPER_ADMIN_PRIVILEGES')
        session['user_name'] = os.getenv('SUPER_ADMIN_NAME')
        session['user_lastname'] = os.getenv('SUPER_ADMIN_LASTNAME')
        session['user_avatar'] = url_for('static', filename=str(
            os.getenv('SUPER_ADMIN_AVATAR')))
        session['user_state'] = os.getenv('SUPER_ADMIN_STATE')
        session['user_public_ip'] = str(get_public_ip())
        session['user_local_ip'] = str(get_local_ip())
        return render_template("home/home.html")

    else:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            remember_me = request.form.get('logged')

            response = requests.get(
                'http://localhost:8080/api/private/user/auth/',
                headers=get_verified_jwt_header(),
                params={
                    'user_username': username,
                    'user_password': password
                }
            )

            if response.status_code == 200:
                if response.json().get('backend_status') == 200:
                    if bool(response.json().get('authenticated')):
                        user = response.json().get('user')
                        if user:
                            if user['user_state'] == 0:
                                flash('Your account is inactive. Please contact the administrator.', 'error')
                                return render_template('auth/login.html')

                            session['user_id'] = user['user_id']
                            session['user_username'] = user['user_username']
                            session['user_privileges'] = user['user_privileges']
                            session['user_name'] = user['user_name']
                            session['user_lastname'] = user['user_lastname']

                            if user['user_privileges'] == 'admin':
                                session['user_avatar'] = url_for('static',
                                                                 filename='img/user_avatars/admin_avatar.svg')
                            elif user['user_privileges'] == 'employee':
                                session['user_avatar'] = url_for('static',
                                                                 filename='img/user_avatars/user_avatar.svg')
                            elif user['user_privileges'] == 'guest':
                                session['user_avatar'] = url_for('static',
                                                                 filename='img/user_avatars/guest_avatar.svg')

                            flash('Welcome back ' + session['user_name'] + ' ' + session['user_lastname'] + '!',
                                  'success')

                            if remember_me:
                                session.permanent = True
                                timeout = timedelta(days=356)
                                current_app.permanent_session_lifetime = timeout
                            else:
                                session.permanent = False
                                timeout = timedelta(hours=1)
                                current_app.permanent_session_lifetime = timeout

                            return render_template('auth/login.html', redirect_to_home=True)
                    else:
                        flash('Invalid credentials', 'error')
            else:
                flash('API Error: An error occurred, please try again later', 'error')
                return redirect(url_for('auth.login'))

        if request.method == 'GET':
            if 'user_id' in session:
                return redirect(url_for('home.home'))
        return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_privileges', None)
    session.pop('user_username', None)
    session.pop('user_name', None)
    session.pop('user_lastname', None)
    session.pop('user_avatar', None)

    return redirect(url_for('auth.login'))


@auth_bp.route('/get/jwt', methods=['GET'])
def get_jwt():
    return jsonify({'jwt': get_verified_jwt_header()}), 200


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
@restrictions.without_login_required
def reset_password():
    if request.method == 'GET':
        return render_template('auth/forgot_password.html')
    elif request.method == 'POST':
        email = request.form.get('email')

        api_url = "http://localhost:8080/api/private/email/reset-password/"

        headers = get_verified_jwt_header()

        payload = {
            'user_email': email
        }

        try:
            response = requests.get(api_url, headers=headers, params=payload)
            if response.status_code == 200:
                if response.json().get('backend_status') == 200:
                    flash('Password reset email sent successfully.', 'success')
                    return render_template('auth/login.html')
                else:
                    flash(response.json().get('message'), 'error')
                    return render_template('auth/login.html')
            else:
                flash('API Error: An error occurred, please try again later', 'error')
                return render_template('auth/login.html')
        except requests.RequestException as e:
            flash(f'API Error: {e}', 'error')
            return render_template('auth/login.html')
