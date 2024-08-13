# Importing Necessary Libraries
from app import functions
from datetime import datetime
# Importing Necessary Libraries

# Importing Necessary Models
from app.blueprints.users.models import User
from app.blueprints.users.models import UserLog
# Importing Necessary Models

# Importing Necessary Entities
from app.blueprints.users.entities import UserEntity
from app.blueprints.users.entities import UserLogEntity


# Importing Necessary Entities

# Class for Users Functions
class UsersFunctions:
    # Constructor
    def __init__(self):  # Constructor
        pass  # Pass the constructor

    # Constructor

    # Function to create a log for an action made by a user
    @staticmethod
    def create_log(user_id, description, action, table):
        # Creating a UserLogEntity object
        user_log = UserLogEntity(
            user_log_id=int(0),
            fk_user_id=int(user_id),
            user_log_description=str(description),
            user_log_action=str(action),
            user_log_table=str(table),
            user_log_date=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            user_log_public_ip=str(functions['get_public_ip']()),
            user_log_local_ip=str(functions['get_local_ip']())
        )
        user_log.validate()  # Validate the UserLogEntity object
        UserLog.add_user_log(user_log)  # Add the log to the database
    # Function to create a log for an action made by a user


# Class for Users Functions

# Create an object for the UsersFunctions class
users_functions = UsersFunctions()
# Create an object for the UsersFunctions class
