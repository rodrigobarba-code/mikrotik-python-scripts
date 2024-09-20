class UserEntity:
    def __init__(
        self,
        user_id,  
        user_username,  
        user_password,  
        user_name,  
        user_lastname,  
        user_privileges,  
        user_state  
    ):
        self.user_id = user_id
        self.user_username = user_username
        self.user_password = user_password
        self.user_name = user_name
        self.user_lastname = user_lastname
        self.user_privileges = user_privileges
        self.user_state = user_state

    def validate(self):
        try:
            assert isinstance(self.user_id, int)  
            assert isinstance(self.user_username, str)  
            assert isinstance(self.user_password, str)  
            assert isinstance(self.user_name, str)  
            assert isinstance(self.user_lastname, str)  
            assert isinstance(self.user_privileges, str)  
            assert isinstance(self.user_state, int)  
        except AssertionError:
            raise ValueError('Invalid User Entity')  
