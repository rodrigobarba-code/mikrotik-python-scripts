class BaseCustomError(Exception):
    pass  

class SiteError(BaseCustomError):
    def __init__(self, message="An error occurred with the Site Section"):
        self.message = message  
        super().__init__(self.message)  

class SiteAlreadyExists(BaseCustomError):
    def __init__(self, site_id, site_name):
        self.site_id = site_id  
        self.site_name = site_name  
        
        self.message = f"Already exists a site with the name '{self.site_name}', with Site ID: {self.site_id}"
        super().__init__(self.message)  
    
class SiteNotFound(BaseCustomError):
    def __init__(self, site_id):
        self.site_id = site_id

        self.message = f"Site with ID: {self.site_id} not found"
        super().__init__(self.message)

class SiteOnBulkDeleteNotFound(BaseCustomError):
    def __init__(self):
        self.message = f"Some sites on the bulk delete list were not found"
        super().__init__(self.message)

class SiteAssociatedWithRouters(BaseCustomError):
    def __init__(self, site_id):
        self.site_id = site_id

        self.message = f"Site with ID: {self.site_id} is associated with at least one Router"
        super().__init__(self.message)

class SiteOnBulkDeleteAssociatedWithRouters(BaseCustomError):
    def __init__(self, site_id):
        self.message = f"Some sites on the bulk delete list are associated with at least one Router"
        super().__init__(self.message)

class SiteSameSegment(BaseCustomError):
    def __init__(self, site_id):
        self.site_id = site_id  
        
        self.message = f"Site with ID: {self.site_id} has the same segment as the new site"
        super().__init__(self.message)  
