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

    @staticmethod
    def without_login_required(f):
        @wraps(f)  # Wraps the function to keep the original function name
        def decorated_function(*args, **kwargs):
            if 'user_id' in session:
                return redirect(url_for('home.home'))
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

    # Decorator for scan requirements
    @staticmethod
    def scan_required(f):
        from websockets.socketio_manager import SocketIOManager

        @wraps(f)  # Wraps the function to keep the original function name
        def decorated_function(*args, **kwargs):
            # If the scan status is not True
            if SocketIOManager.get_scan_status() == 0:
                return redirect(url_for('home.home'))  # Redirect to the loading screen

            return f(*args, **kwargs)  # Return the function

        return decorated_function  # Return the decorated function
    # Decorator for scan requirements

    # Decorator for scan in progress requirements
    @staticmethod
    def redirect_to_loading_screen(f):
        from websockets.socketio_manager import SocketIOManager

        @wraps(f)  # Wraps the function to keep the original function name
        def decorated_function(*args, **kwargs):
            # If the scan status is not True
            if SocketIOManager.get_scan_status() == 1:
                return redirect(url_for('router_scan.loading_screen'))  # Redirect to the loading screen

            return f(*args, **kwargs)  # Return the function

        return decorated_function  # Return the decorated function
    # Decorator for scan in progress requirements

# Class for Requirements Decorators
