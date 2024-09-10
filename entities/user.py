# Description: User Entities

# Class for User Entity
class UserEntity:
    # Constructor
    def __init__(
        self,
        user_id,  # User ID
        user_username,  # User Username
        user_password,  # User Password
        user_name,  # User Name
        user_lastname,  # User Lastname
        user_privileges,  # User Privileges
        user_state  # User State
    ):
        self.user_id = user_id
        self.user_username = user_username
        self.user_password = user_password
        self.user_name = user_name
        self.user_lastname = user_lastname
        self.user_privileges = user_privileges
        self.user_state = user_state
    # Constructor

    # Validate User Entity
    def validate(self):
        try:
            assert isinstance(self.user_id, int)  # Verify if Router ID is an Integer
            assert isinstance(self.user_username, str)  # Verify if Router Name is a String
            assert isinstance(self.user_password, str)  # Verify if Router Description is a String
            assert isinstance(self.user_name, str)  # Verify if Router Brand is a String
            assert isinstance(self.user_lastname, str)  # Verify if Router Model is a String
            assert isinstance(self.user_privileges, str)  # Verify if Foreign Key Site ID is an Integer
            assert isinstance(self.user_state, int)  # Verify if Router IP is a String
        except AssertionError:
            raise ValueError('Invalid User Entity')  # Raise an Exception if the Entity is Invalid
    # Validate User Entity
# Class for User Entity
