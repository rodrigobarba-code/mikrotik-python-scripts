class UserEntity:
    def __init__(
        self,
        user_id: int,
        user_username: str = None,
        user_email: str = None,
        user_password: str = None,
        user_name: str = None,
        user_lastname: str = None,
        user_privileges: str = 'employee',
        user_state: int = 1
    ):
        self.user_id = user_id
        self.user_username = user_username
        self.user_email = user_email
        self.user_password = user_password
        self.user_name = user_name
        self.user_lastname = user_lastname
        self.user_privileges = user_privileges
        self.user_state = user_state

    def validate(self):
        try:
            assert isinstance(self.user_id, int)  
            assert isinstance(self.user_username, str)
            assert isinstance(self.user_email, str)
            assert isinstance(self.user_password, str)  
            assert isinstance(self.user_name, str)  
            assert isinstance(self.user_lastname, str)  
            assert isinstance(self.user_privileges, str)  
            assert isinstance(self.user_state, int)  
        except AssertionError:
            raise ValueError('Invalid User Entity')  
