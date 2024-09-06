# Importing the necessary libraries
from functools import wraps
from flask import session, redirect, url_for


# Importing the necessary libraries

# Class for requirements decorators, used to restrict access to certain routes
class RequirementsDecorators:
    # Decorator for login requirements
    @staticmethod
    def login_required(f):
        @wraps(f)  # Wraps the function to keep the original function name
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:  # If the user_id is not in the session
                return redirect(url_for('auth.login'))  # Redirect to the login page
            return f(*args, **kwargs)  # Return the function

        return decorated_function  # Return the decorated function

    # Decorator for login requirements

    # Decorator for admin requirements
    @staticmethod
    def admin_required(f):
        @wraps(f)  # Wraps the function to keep the original function name
        def decorated_function(*args, **kwargs):
            # If the user_privileges is not in the session or the user_privileges is not 'admin'
            if 'user_privileges' not in session or session['user_privileges'] not in ['admin', 'superadmin']:
                return redirect(url_for('auth.login'))  # Redirect to the login page
            return f(*args, **kwargs)  # Return the function

        return decorated_function  # Return the decorated function

    # Decorator for admin requirements

# Class for Requirements Decorators
