import os, bcrypt
from . import auth_bp
from datetime import timedelta
from dotenv import load_dotenv
from models.users.models import User
from app.functions import get_verified_jwt_header
from app.functions import get_local_ip, get_public_ip
from models.users.functions import users_functions as functions
from flask import render_template, redirect, url_for, flash, request, session, current_app, jsonify

load_dotenv()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():  
    dev_mode = os.getenv('DEVELOPMENT_MODE', 'True').lower() in ['true', '1', 't']  
    if dev_mode:  
        session['user_id'] = 1  
        session['user_username'] = os.getenv('SUPER_ADMIN_USER')  
        session['user_privileges'] = os.getenv('SUPER_ADMIN_PRIVILEGES')  
        session['user_name'] = os.getenv('SUPER_ADMIN_NAME')  
        session['user_lastname'] = os.getenv('SUPER_ADMIN_LASTNAME')  
        session['user_avatar'] = url_for('static', filename=str(
            os.getenv('SUPER_ADMIN_AVATAR')))  
        session['user_state'] = os.getenv('SUPER_ADMIN_STATE')
        session['user_public_ip'] = str(get_public_ip())  
        session['user_local_ip'] = str(get_local_ip())
        functions.create_log(session['user_id'], 'Super Admin logged in', 'LOGIN', 'users')
        return render_template("home/home.html")
    else:
        if request.method == 'POST':  
            username = request.form.get('username')  
            password = request.form.get('password').encode('utf-8')  
            remember_me = request.form.get('logged')
            user = User.query.filter_by(user_username=username).first()  
            if user:
                if user.user_state == 0:  
                    flash('Your account is inactive. Please contact the administrator.', 'error')
                    return render_template('auth/login.html')
                if bcrypt.checkpw(password, user.user_password):  
                    session['user_id'] = user.user_id  
                    session['user_username'] = user.user_username  
                    session['user_privileges'] = user.user_privileges  
                    session['user_name'] = user.user_name  
                    session['user_lastname'] = user.user_lastname  
                    session['user_public_ip'] = str(get_public_ip())  
                    session['user_local_ip'] = str(get_local_ip())
                if user.user_privileges == 'admin':  
                    session['user_avatar'] = url_for('static',
                                                     filename='img/user_avatars/admin_avatar.svg')  
                elif user.user_privileges == 'employee':  
                    session['user_avatar'] = url_for('static',
                                                     filename='img/user_avatars/user_avatar.svg')  
                elif user.user_privileges == 'guest':  
                    session['user_avatar'] = url_for('static',
                                                     filename='img/user_avatars/guest_avatar.svg')
                functions.create_log(session['user_id'], 'User logged in', 'LOGIN', 'users')  
                flash('Welcome back ' + user.user_name + ' ' + user.user_lastname + '!',
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
        if request.method == 'GET':  
            if 'user_id' in session:  
                return redirect(url_for('home.home'))  
        return render_template('auth/login.html')  

@auth_bp.route('/logout')
def logout():
    functions.create_log(session['user_id'], 'User logged out', 'LOGOUT', 'users')  

    session.pop('user_id', None)  
    session.pop('user_privileges', None)  
    session.pop('user_username', None)  
    session.pop('user_name', None)  
    session.pop('user_lastname', None)  
    session.pop('user_avatar', None)  
    session.pop('user_public_ip', None)  
    session.pop('user_local_ip', None)  

    return redirect(url_for('auth.login'))

@auth_bp.route('/get/jwt', methods=['GET'])
def get_jwt():
    return jsonify({'jwt': get_verified_jwt_header()}), 200
