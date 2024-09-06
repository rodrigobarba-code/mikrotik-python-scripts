# Importing Necessary Libraries
from flask import session
from datetime import datetime
from app.extensions import func
# Importing Necessary Libraries

# Importing Necessary Entities
from app.blueprints.users.entities import UserLogEntity
# Importing Necessary Entities

# Importing Required Exceptions
from app.blueprints.users.exceptions import *
# Importing Required Exceptions

# Class for Users Functions
class UsersFunctions:
    # Constructor
    def __init__(self):  # Constructor
        pass  # Pass the constructor
    # Constructor

    # Function to create a log for an action made by a user
    @staticmethod
    def create_log(user_id, description, action, table):
        from app.blueprints.users.models import UserLog  # Importing the UserLog model
        # Creating a UserLogEntity object
        user_log = UserLogEntity(
            user_log_id=int(),
            rk_user_id=int(user_id),
            rk_user_username=str(session['user_username']),
            rk_user_name=str(session['user_name']),
            rk_user_lastname=str(session['user_lastname']),
            user_log_description=str(description),
            user_log_action=str(action),
            user_log_table=str(table),
            user_log_date=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            user_log_public_ip=str(session['user_public_ip']),
            user_log_local_ip=str(session['user_local_ip'])
        )
        user_log.validate()  # Validate the UserLogEntity object
        UserLog.add_user_log(user_log)  # Add the log to the database
    # Function to create a log for an action made by a user

    # Function to validate all the User Details
    @staticmethod
    def validate_user(user, operation, model) -> bool:
        try:
            if operation in ["insert", "update"]:  # Check if the operation is insert or update
                if operation == "update":  # If the operation is updated
                    existing_user = model.query.get(user.user_id)  # Get the existing user
                    if not existing_user:  # Check if the existing user is not found
                        raise UserNotFound(user.user_id)  # Raise User Not Found Exception
                # Check if the user username is already taken
                if model.query.filter(func.lower(model.user_username) == func.lower(user.user_username)).first() and \
                        model.query.filter(func.lower(model.user_username) == func.lower(user.user_username)).first().user_id != user.user_id:
                    raise UserAlreadyExists(  # Raise User Already Exists Exception
                        user_id=model.query.filter(  # Get the user id
                            func.lower(model.user_username) == func.lower(user.user_username)).first().user_id,
                        user_username=user.user_username  # Get the user username
                    )
                return True  # Return True
            # Check if the operation is deleted or get
            elif operation in ["delete", "get"]:  # If the operation is deleted or get
                if not model.query.filter_by(user_id=user.user_id).first():  # Check if the user is not found
                    raise UserNotFound(user.user_id)  # Raise User Not Found Exception
                return True  # Return True
            return False  # Return False if the operation is not found
        except (UserNotFound, UserAlreadyExists) as e:  # Catch the exceptions
            raise e  # Raise the exception
        except Exception:  # Catch the exception
            raise UserError()  # Raise Router Error Exception
    # Function to validate all the User Details
# Class for Users Functions

# Create an object for the UsersFunctions class
users_functions = UsersFunctions()
# Create an object for the UsersFunctions class
