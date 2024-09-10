# Description: Exceptions for the Site Blueprint

# Base Exception for the Site Blueprint
class BaseCustomError(Exception):
    pass  # Pass the BaseCustomError class
# Base Exception for the Site Blueprint

# Site Error Exception
class SiteError(BaseCustomError):
    # Constructor
    def __init__(self, message="An error occurred with the Site Section"):
        self.message = message  # Set the message
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# Site Error Exception

# Site Already Exists Exception
class SiteAlreadyExists(BaseCustomError):
    # Constructor
    def __init__(self, site_id, site_name):
        self.site_id = site_id  # Set the site ID
        self.site_name = site_name  # Set the site name
        # Show the error message
        self.message = f"Already exists a site with the name '{self.site_name}', with Site ID: {self.site_id}"
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# Site Already Exists Exception

# Site Not Found Exception
class SiteNotFound(BaseCustomError):
    # Constructor
    def __init__(self, site_id):
        self.site_id = site_id  # Set the site ID
        # Show the error message
        self.message = f"Site with ID: {self.site_id} not found"
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# Site Not Found Exception

# Site Associated With Routers
class SiteAssociatedWithRouters(BaseCustomError):
    # Constructor
    def __init__(self, site_id):
        self.site_id = site_id  # Set the site ID
        # Show the error message
        self.message = f"Site with ID: {self.site_id} is associated with at least one Router"
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# Site Associated With Routers

# Site Same Segment Exception
class SiteSameSegment(BaseCustomError):
    # Constructor
    def __init__(self, site_id):
        self.site_id = site_id  # Set the site ID
        # Show the error message
        self.message = f"Site with ID: {self.site_id} has the same segment as the new site"
        super().__init__(self.message)  # Call the super constructor with the message as parameter
    # Constructor
# Site Same Segment Exception
