# Importing necessary modules

import bcrypt, os
from datetime import timedelta  # Importing the timedelta module from the datetime module to set the session timeout
from app.functions import get_local_ip, get_public_ip
from models.users.functions import users_functions as functions
from flask import render_template, redirect, url_for, flash, request, session, current_app
from dotenv import load_dotenv
# Importing necessary modules

# Importing necessary decorators
# Importing necessary decorators

# Importing necessary models
from models.users.models import User
# Importing necessary models

from . import auth_bp  # Importing the blueprint instance

# Load environment variables from .env file
load_dotenv()


# Auth Login Route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():  # Login route
    dev_mode = os.getenv('DEVELOPMENT_MODE', 'True').lower() in ['true', '1', 't']  # Convert to boolean
    if dev_mode:  # If the development mode is enabled):
        session['user_id'] = 1  # Set the user_id session variable
        session['user_username'] = os.getenv('SUPER_ADMIN_USER')  # Set the user_username session variable
        session['user_privileges'] = os.getenv('SUPER_ADMIN_PRIVILEGES')  # Set the user_privileges session variable
        session['user_name'] = os.getenv('SUPER_ADMIN_NAME')  # Set the user_name session variable
        session['user_lastname'] = os.getenv('SUPER_ADMIN_LASTNAME')  # Set the user_lastname session variable
        session['user_avatar'] = url_for('static', filename=str(
            os.getenv('SUPER_ADMIN_AVATAR')))  # Set the user_avatar session variable
        session['user_state'] = os.getenv('SUPER_ADMIN_STATE')
        session['user_public_ip'] = str(get_public_ip())  # Set the user_public_ip session variable
        session['user_local_ip'] = str(get_local_ip())  # Set the user_local_ip session variable

        functions.create_log(session['user_id'], 'Super Admin logged in', 'LOGIN', 'users')  # Create a log

        return render_template("home/home.html")  # Redirect the user to the home page

    else:
        if request.method == 'POST':  # If the request method is POST
            username = request.form.get('username')  # Get the username from the form
            password = request.form.get('password').encode('utf-8')  # Get the password from the form and encode it
            remember_me = request.form.get('logged')  # Get the "Remember me" checkbox value

            user = User.query.filter_by(user_username=username).first()  # Get the user from the database
            if user:
                if user.user_state == 0:  # Check if the user is inactive
                    flash('Your account is inactive. Please contact the administrator.', 'error')
                    return render_template('auth/login.html')  # Render the login page with an error message

                if bcrypt.checkpw(password, user.user_password):  # If the user exists and the password is correct
                    session['user_id'] = user.user_id  # Set the user_id session variable
                    session['user_username'] = user.user_username  # Set the user_username session variable
                    session['user_privileges'] = user.user_privileges  # Set the user_privileges session variable
                    session['user_name'] = user.user_name  # Set the user_name session variable
                    session['user_lastname'] = user.user_lastname  # Set the user_lastname session variable
                    session['user_public_ip'] = str(get_public_ip())  # Set the user_public_ip session variable
                    session['user_local_ip'] = str(get_local_ip())  # Set the user_local_ip session variable

                if user.user_privileges == 'admin':  # Set the user_avatar session variable based on the user's privileges
                    session['user_avatar'] = url_for('static',
                                                     filename='img/user_avatars/admin_avatar.svg')  # Set the user_avatar session variable
                elif user.user_privileges == 'employee':  # Set the user_avatar session variable based on the user's privileges
                    session['user_avatar'] = url_for('static',
                                                     filename='img/user_avatars/user_avatar.svg')  # Set the user_avatar session variable
                elif user.user_privileges == 'guest':  # Set the user_avatar session variable based on the user's privileges
                    session['user_avatar'] = url_for('static',
                                                     filename='img/user_avatars/guest_avatar.svg')  # Set the user_avatar session variable

                functions.create_log(session['user_id'], 'User logged in', 'LOGIN', 'users')  # Create a log
                flash('Welcome back ' + user.user_name + ' ' + user.user_lastname + '!',
                      'success')  # Flash a success message

                if remember_me:  # If the "Remember me" checkbox is checked
                    session.permanent = True  # Make the session permanent (1 year)
                    timeout = timedelta(days=356)  # Set session timeout to 1 year
                    current_app.permanent_session_lifetime = timeout  # Set the session timeout
                else:  # If the "Remember me" checkbox is not checked
                    session.permanent = False  # Make the session non-permanent
                    timeout = timedelta(hours=1)  # Set session timeout to 10 seconds for testing
                    current_app.permanent_session_lifetime = timeout  # Set the session timeout

                return render_template('auth/login.html', redirect_to_home=True)  # Render the login page
            else:  # If the user does not exist or the password is incorrect
                flash('Invalid credentials', 'error')  # Flash an error message
        if request.method == 'GET':  # If the request method is GET
            if 'user_id' in session:  # If the user is already logged in and tries to access the login page
                return redirect(url_for('home.home'))  # Redirect the user to the home page
        return render_template('auth/login.html')  # Render the login page


# Auth Login Route

# Auth Logout Route
@auth_bp.route('/logout')
def logout():
    functions.create_log(session['user_id'], 'User logged out', 'LOGOUT', 'users')  # Create a log

    # Remove all user information from client session
    session.pop('user_id', None)  # Remove the user_id session variable
    session.pop('user_privileges', None)  # Remove the user_privileges session variable
    session.pop('user_username', None)  # Remove the user_username session variable
    session.pop('user_name', None)  # Remove the user_name session variable
    session.pop('user_lastname', None)  # Remove the user_lastname session variable
    session.pop('user_avatar', None)  # Remove the user_avatar session variable
    session.pop('user_public_ip', None)  # Remove the user_public_ip session variable
    session.pop('user_local_ip', None)  # Remove the user_local_ip session variable
    # Remove all user information from client session

    return redirect(url_for('auth.login'))  # Redirect the user to the login page
# Auth Logout Route
