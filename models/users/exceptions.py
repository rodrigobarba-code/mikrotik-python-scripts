class BaseCustomError(Exception):
    pass  

class UserError(BaseCustomError):
    def __init__(self, message="An error occurred with the User Section"):
        self.message = message  
        super().__init__(self.message)

class UserNotFound(UserError):
    def __init__(self, user_id):
        self.message = f"User with ID {user_id} not found"  
        super().__init__(self.message)
    
class UserAlreadyExists(UserError):
    def __init__(self, user_id, user_username):
        self.message = f"User with ID {user_id} and Username {user_username} already exists"  
        super().__init__(self.message)

class UserEmailAlreadyExists(UserError):
    def __init__(self, user_id, user_email):
        self.message = f"User with ID {user_id} and Email {user_email} already exists"
        super().__init__(self.message)
    
class UserLogError(BaseCustomError):
    def __init__(self, message="An error occurred with the User Log Section"):
        self.message = message  
        super().__init__(self.message)

class UserLogDatabaseError(UserLogError):
    def __init__(self, message="An error occurred with the database of User Log Section"):
        self.message = message  
        super().__init__(self.message)
