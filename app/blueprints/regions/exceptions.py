# Description: Exceptions for the Region Blueprint

# Base Exception for the Region Blueprint
class BaseCustomError(Exception):
    pass  # Pass the BaseCustomError class
# Base Exception for the Region Blueprint

# Region Error Exception
class RegionError(BaseCustomError):
    # Constructor
    def __init__(self, message="An error occurred with the Region Section"):
        self.message = message  # Set the message
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# Region Error Exception

# Region Already Exists Exception
class RegionAlreadyExists(BaseCustomError):
    # Constructor
    def __init__(self, region_id, region_name):
        self.region_id = region_id  # Set the region ID
        self.region_name = region_name  # Set the region name
        # Show the error message
        self.message = f"Already exists a region with the name '{self.region_name}', with Region ID: {self.region_id}"
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# Region Already Exists Exception

# Region Not Found Exception
class RegionNotFound(BaseCustomError):
    # Constructor
    def __init__(self, region_id):
        self.region_id = region_id  # Set the region ID
        # Show the error message
        self.message = f"Region with ID: {self.region_id} not found"
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# Region Not Found Exception

# Region Associated With Site Exception
class RegionAssociatedWithSite(BaseCustomError):
    # Constructor
    def __init__(self, region_id, site_id):
        self.region_id = region_id  # Set the region ID
        self.site_id = site_id  # Set the site ID
        # Show the error message
        self.message = f"Region with ID: {self.region_id} is associated with a Site with ID: {self.site_id}"
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# Region Associated With Site Exception
