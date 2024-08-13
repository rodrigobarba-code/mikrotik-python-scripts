# Importing necessary modules
import bcrypt
from flask import render_template, redirect, url_for, flash, request, session
# Importing necessary modules

# Importing necessary decorators
from app.decorators import RequirementsDecorators as restriction
# Importing necessary decorators

# Importing necessary models
from app.blueprints.users.models import User
# Importing necessary models

from . import auth_bp  # Importing the blueprint instance

# Auth Login Route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # If the request method is POST
        username = request.form.get('username')  # Get the username from the form
        password = request.form.get('password').encode('utf-8')  # Get the password from the form and encode it
        # Query the database for the user to check if it exists
        user = User.query.filter_by(user_username=username).first()
        if user:  # If the user exists, will try to check the password, otherwise will return an error message
            if bcrypt.checkpw(password, user.user_password):  # Check the password hash with the one in the database
                # Create the session variables for the user
                session['user_id'] = user.user_id  # Identify the user by the user_id
                session['user_username'] = user.user_username  # Identify the user by the user_username
                session['user_privileges'] = user.user_privileges  # Identify the user by the user_privileges
                session['user_name'] = user.user_name  # Indentify the user by the user_name
                session['user_lastname'] = user.user_lastname  # Indentify the user by the user_lastname
                # Create the session variables for the user

                # Set the user avatar based on the user privileges
                if user.user_privileges == 'admin':  # If the user is an admin, will set the admin avatar
                    session['user_avatar'] = url_for('static', filename='img/user_avatars/admin_avatar.svg')
                elif user.user_privileges == 'employee':  # If the user is an employee, will set the employee avatar
                    session['user_avatar'] = url_for('static', filename='img/user_avatars/user_avatar.svg')
                elif user.user_privileges == 'guest':
                    session['user_avatar'] = url_for('static', filename='img/user_avatars/guest_avatar.svg')
                return redirect(url_for('home.home'))
                # Set the user avatar based on the user privileges
            else:
                flash('Invalid password, are you sure you typed it correctly?')  # If the password is incorrect, will return an error message
        else:
            flash('Invalid username, maybe you need to register')  # If the user does not exist, will return an error message
    return render_template('auth/login.html')  # If the request method is GET, will render the login page
# Auth Login Route

# Auth Logout Route
@auth_bp.route('/logout')
def logout():
    # Remove all user information from client session
    session.pop('user_id', None)  # Remove the user_id session variable
    session.pop('user_privileges', None)  # Remove the user_privileges session variable
    session.pop('user_username', None)  # Remove the user_username session variable
    session.pop('user_name', None)  # Remove the user_name session variable
    session.pop('user_lastname', None)  # Remove the user_lastname session variable
    session.pop('user_avatar', None)  # Remove the user_avatar session variable
    # Remove all user information from client session

    return redirect(url_for('auth.login'))  # Redirect the user to the login page
# Auth Logout Route
