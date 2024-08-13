# Description: Users Entities

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

# Class for User Log Entity
class UserLogEntity:
    # Constructor
    def __init__(
        self,
        user_log_id,  # User Log ID
        rk_user_id,  # Reference Key User ID
        rk_user_username,  # Reference Key User Username
        rk_user_name,  # Reference Key Name
        rk_user_lastname,  # Reference Key User Lastname
        user_log_description,  # User Log Description
        user_log_action,  # User Log Action
        user_log_table,  # User Log Table
        user_log_date,  # User Log Date
        user_log_public_ip,  # User Log Public IP
        user_log_local_ip  # User Log Local IP
    ):
        self.user_log_id = user_log_id
        self.rk_user_id = rk_user_id
        self.rk_user_username = rk_user_username
        self.rk_user_name = rk_user_name
        self.rk_user_lastname = rk_user_lastname
        self.user_log_description = user_log_description
        self.user_log_action = user_log_action
        self.user_log_table = user_log_table
        self.user_log_date = user_log_date
        self.user_log_public_ip = user_log_public_ip
        self.user_log_local_ip = user_log_local_ip
    # Constructor

    # Validate User Log Entity
    def validate(self):
        try:
            assert isinstance(self.user_log_id, int)  # Verify if Router ID is an Integer
            assert isinstance(self.rk_user_id, int)  # Verify if Router ID is an Integer
            assert isinstance(self.rk_user_username, str)  # Verify if Router Name is a String
            assert isinstance(self.rk_user_name, str)  # Verify if Router Description is a String
            assert isinstance(self.rk_user_lastname, str)  # Verify if Router Brand is a String
            assert isinstance(self.user_log_description, str)  # Verify if Router Name is a String
            assert isinstance(self.user_log_action, str)  # Verify if Router Description is a String
            assert isinstance(self.user_log_table, str)  # Verify if Router Brand is a String
            assert isinstance(self.user_log_public_ip, str)  # Verify if Foreign Key Site ID is an Integer
            assert isinstance(self.user_log_local_ip, str)  # Verify if Router IP is a String
        except AssertionError:
            raise ValueError('Invalid User Log Entity')  # Raise an Exception if the Entity is Invalid
    # Validate User Log Entity
# Class for User Log Entity
