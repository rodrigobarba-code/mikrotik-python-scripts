# Description: Exceptions for the User Blueprint

# Base Exception for the User Blueprint
class BaseCustomError(Exception):
    pass  # Pass the BaseCustomError class
# Base Exception for the User Blueprint

# User Error Exception
class UserError(BaseCustomError):
    # Constructor
    def __init__(self, message="An error occurred with the User Section"):
        self.message = message  # Set the message
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# User Error Exception

# User Not Found Exception
class UserNotFound(UserError):
    # Constructor
    def __init__(self, user_id):
        self.message = f"User with ID {user_id} not found"  # Set the message
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# User Not Found Exception

# User Already Exists Exception
class UserAlreadyExists(UserError):
    # Constructor
    def __init__(self, user_id, user_username):
        self.message = f"User with ID {user_id} and Username {user_username} already exists"  # Set the message
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# User Already Exists Exception

# User Log Error Exception
class UserLogError(BaseCustomError):
    # Constructor
    def __init__(self, message="An error occurred with the User Log Section"):
        self.message = message  # Set the message
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# User Log Error Exception

# User Log Database Error Exception
class UserLogDatabaseError(UserLogError):
    # Constructor
    def __init__(self, message="An error occurred with the database of User Log Section"):
        self.message = message  # Set the message
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# User Log Database Error Exception
