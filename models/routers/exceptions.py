# Description: Exceptions for the Router Blueprint

# Base Exception for the Router Blueprint
class BaseCustomError(Exception):
    pass  # Pass the BaseCustomError class
# Base Exception for the Router Blueprint

# Router Error Exception
class RouterError(BaseCustomError):
    # Constructor
    def __init__(self, message="An error occurred with the Router Section"):
        self.message = message  # Set the message
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# Router Error Exception

# Router Already Exists Exception
class RouterAlreadyExists(BaseCustomError):
    # Constructor
    def __init__(self, router_id, router_name):
        self.router_id = router_id  # Set the router ID
        self.router_name = router_name  # Set the router name
        # Show the error message
        self.message = f"Already exists a router with the name '{self.router_name}', with Router ID: {self.router_id}"
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# Router Already Exists Exception

# Router Not Found Exception
class RouterNotFound(BaseCustomError):
    # Constructor
    def __init__(self, router_id):
        self.router_id = router_id  # Set the router ID
        # Show the error message
        self.message = f"Router with ID: {self.router_id} not found"
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# Router Not Found Exception

# Router IP Already Exists Exception
class RouterIPAlreadyExists(BaseCustomError):
    # Constructor
    def __init__(self, router_id, router_ip):
        self.router_id = router_id  # Set the router ID
        self.router_ip = router_ip  # Set the router IP
        # Show the error message
        self.message = f"A router with the IP: {self.router_ip} already exists, with Router ID: {self.router_id}"
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# Router IP Already Exists Exception

# Router MAC Already Exists Exception
class RouterMACAlreadyExists(BaseCustomError):
    # Constructor
    def __init__(self, router_id, router_mac):
        self.router_id = router_id  # Set the router ID
        self.router_mac = router_mac  # Set the router MAC
        # Show the error message
        self.message = f"A router with the MAC: {self.router_mac} already exists, with Router ID: {self.router_id}"
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# Router MAC Already Exists Exception

# Router IP Not Valid Exception
class RouterIPNotValid(BaseCustomError):
    # Constructor
    def __init__(self, router_ip):
        self.router_ip = router_ip  # Set the router IP
        # Show the error message
        self.message = f"The IP: {self.router_ip} is not a valid IP"
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# Router IP Not Valid Exception

# Router MAC Not Valid Exception
class RouterMACNotValid(BaseCustomError):
    # Constructor
    def __init__(self, router_mac):
        self.router_mac = router_mac  # Set the router MAC
        # Show the error message
        self.message = f"The MAC: {self.router_mac} is not a valid MAC"
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# Router MAC Not Valid Exception
