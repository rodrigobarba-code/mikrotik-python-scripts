# Description: Exceptions for the IP Addresses Blueprint

# Base Exception for the IP Addresses Blueprint
class BaseCustomError(Exception):
    pass  # Pass the BaseCustomError class
# Base Exception for the IP Addresses Blueprint

# IP Addresses Error Exception
class IPAddressesError(BaseCustomError):
    # Constructor
    def __init__(self, message="An error occurred with the IP Addresses Blueprint."):
        self.message = message  # Set the message
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# IP Addresses Error Exception

# IP Segment Not Found Exception
class IPSegmentNotFound(IPAddressesError):
    # Constructor
    def __init__(self, ip_segment_id, message="The IP Segment was not found."):
        self.ip_segment_id = ip_segment_id
        self.message = message
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# IP Segment Not Found Exception

# IP Segment Already Exists Exception
class IPSegmentAlreadyExists(IPAddressesError):
    # Constructor
    def __init__(self, message="The IP Segment already exists."):
        self.message = message  # Set the message
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# IP Segment Already Exists Exception
