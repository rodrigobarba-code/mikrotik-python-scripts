# Description: Users Routes for the Users Blueprint

# Importing Required Local Modules
from . import users_bp  # Import the sites Blueprint
from app.blueprints.users.functions import users_functions as functions  # Import the users functions object
# Importing Required Local Modules

# Importing Required Libraries
from flask import render_template, redirect, url_for, flash, request, jsonify, session
# Importing Required Libraries

# Importing Required Decorators
from app.decorators import RequirementsDecorators as restriction
# Importing Required Decorators

# Importing Required Entities
from app.blueprints.users.entities import UserEntity
# Importing Required Entities

# Importing Required Models
from app.blueprints.users.models import User
from app.blueprints.users.models import UserLog
# Importing Required Models

# Importing Required Functions
from .functions import users_functions as functions
# Importing Required Functions

# Users Main Route
@users_bp.route('/')
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def users():
    try:
        return render_template(  # Render the users template
            'users/users.html',  # Render the users template
            user_list=User.get_users(),  # Pass the user list to the template
            user=None  # Pass None to the template
        )
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('users.users'))  # Redirect to the sites route
# Users Main Route

# Users Add Route
@users_bp.route('/add', methods=['GET', 'POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def add_user():
    if request.method == 'POST':  # If the request method is POST
        try:  # Try to add the user
            user = UserEntity(
                user_id=None,  # Set the id to None
                user_username=request.form['user_username'],  # Set the username
                user_password=request.form['user_password'],  # Set the password
                user_name=request.form['user_name'],  # Set the name
                user_lastname=request.form['user_lastname'],  # Set the lastname
                user_privileges=request.form['user_privileges'],  # Set the privileges
                user_state=request.form['user_state']  # Set the status
            )
            User.add_user(user)  # Add the user
            flash('User added successfully', 'success')  # Flash a success message
            functions.create_log(session['user_id'], 'User added', 'INSERT', 'users')  # Create a log
        except Exception as e:  # If an exception occurs
            flash(str(e), 'danger')  # Flash the exception message
        return redirect(url_for('users.users'))  # Redirect to the users route
    try:
        return render_template(
            'users/form_users.html',  # Render the users template
            user_list=User.get_users(),  # Pass the user list to the template
            user=None  # Pass None to the
        )
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('users.users'))  # Redirect to the users route
# Users Add Route

# Users Update Route
@users_bp.route('/update/<user_id>', methods=['GET', 'POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def update_user(user_id):
    if request.method == 'POST':  # If the request method is POST
        try:  # Try to update the user
            user = UserEntity(
                user_id=user_id,  # Set the id
                user_username=request.form['user_username'],  # Set the username
                user_password=request.form['user_password'],  # Set the password
                user_name=request.form['user_name'],  # Set the name
                user_lastname=request.form['user_lastname'],  # Set the lastname
                user_privileges=request.form['user_privileges'],  # Set the privileges
                user_state=request.form['user_state']  # Set the status
            )
            User.update_user(user)  # Update the user
            flash('User updated successfully', 'success')  # Flash a success message
            functions.create_log(session['user_id'], 'User updated', 'UPDATE', 'users')  # Create a log
        except Exception as e:  # If an exception occurs
            flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('users.users'))  # Redirect to the users route
    try:
        user_list = User.get_users()  # Get the user list
        user = User.get_user(user_id)  # Get the user
        return render_template(
            'users/form_users.html',  # Render the users template
            user_list=user_list,  # Pass the user list to the template
            user=user  # Pass the user to the template
        )
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('users.users'))  # Redirect to the sites route
# Users Update Route

# Users Delete Route
@users_bp.route('/delete/<int:user_id>', methods=['GET'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def delete_user(user_id):
    try:  # Try to delete the user
        User.delete_user(user_id)  # Delete the user
        flash('User deleted successfully', 'success')  # Flash a success message
        functions.create_log(session['user_id'], 'User deleted', 'DELETE', 'users')  # Create a log
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
    return redirect(url_for('users.users'))  # Redirect to the users route
# User Delete Route

# Users Bulk Delete Route
@users_bp.route('/delete/bulk', methods=['POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def bulk_delete_user():
    data = request.get_json()  # Get the JSON data
    user_ids = data.get('items_ids', [])  # Get the user IDs
    try:
        flag = 0  # Set the flag to 0
        for user_id in user_ids:  # For each user ID
            User.delete_user(user_id)  # Delete the user
            flag += 1  # Increment the flag
        flash(f'{flag} Users deleted successfully', 'success')  # Flash a success message
        functions.create_log(session['user_id'], f'{flag} Users deleted', 'DELETE', 'users')  # Create a log
        return jsonify({'message': 'Users deleted successfully'}), 200  # Return a success message
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return jsonify({'message': 'Failed to delete users', 'error': str(e)}), 500  # Return an error message
# Users Bulk Delete Route

# Users Delete All Route
@users_bp.route('/delete_all_users', methods=['POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def delete_all_users():
    try:  # Try to delete all users
        User.delete_all_users()  # Delete all users
        flash('All Routers Deleted Successfully', 'success')  # Flash a success message
        functions.create_log(session['user_id'], 'All Users deleted', 'DELETE', 'users')  # Create a log
        return jsonify({'message': 'Routers deleted successfully'}), 200  # Return a success message
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return jsonify({'message': 'Failed to delete routers', 'error': str(e)}), 500  # Return an error message
# Users Delete All Route

# Users Log Route
@users_bp.route('/log', methods=['GET'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def log():
    try:
        return render_template(  # Render the log template
            'users/log.html',  # Render the log template
            user_log_list=UserLog.get_user_logs(),  # Pass the user log list to the template
            user_log=None  # Pass None to the template
        )
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('users.log'))  # Redirect to the log route
# Users Log Route

# Users Delete By Date Users Log Route
@users_bp.route('/delete_from_date_user_log', methods=['POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def delete_from_date_user_log():
    data = request.get_json()  # Get the JSON data
    date = data.get('date', None)  # Get the date
    date += ' 23:59:59'  # Add the time
    try:
        flag = UserLog.delete_from_date_user_log(date)  # Delete the user logs
        if flag == 0:  # If no user logs were deleted
            flash('No User Logs Found', 'danger')  # Flash a warning message
            return jsonify({'message': 'No User Logs Found'}), 200  # Return a warning message
        else:
            flash(f'{flag} User Logs deleted successfully', 'success')  # Flash a success message
            return jsonify({'message': 'User Logs deleted successfully'}), 200  # Return a success message
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return jsonify({'message': 'User Logs Failed to Delete', 'error': str(e)}), 500  # Return an error message
# Users Delete By Date Users Log Route
