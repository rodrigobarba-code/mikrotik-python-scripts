class BaseCustomError(Exception):
    pass  

class RegionError(BaseCustomError):
    def __init__(self, message="An error occurred with the Region Section"):
        self.message = message  
        super().__init__(self.message)  

class RegionAlreadyExists(BaseCustomError):
    def __init__(self, region_id, region_name):
        self.region_id = region_id  
        self.region_name = region_name
        self.message = f"Already exists a region with the name '{self.region_name}', with Region ID: {self.region_id}"
        super().__init__(self.message)  

class RegionNotFound(BaseCustomError):
    def __init__(self, region_id):
        self.region_id = region_id
        self.message = f"Region with ID: {self.region_id} not found"
        super().__init__(self.message)  

class RegionOnBulkDeleteNotFound(BaseCustomError):
    def __init__(self):
        self.message = f"Some Region on the Bulk Delete List were not found"
        super().__init__(self.message)  

class RegionOnBulkDeleteIsAssociatedWithSite(BaseCustomError):
    def __init__(self):
        self.message = f"Region on the Bulk Delete List is associated with a Site"
        super().__init__(self.message)  

class RegionAssociatedWithSite(BaseCustomError):
    def __init__(self, region_id, site_id):
        self.region_id = region_id  
        self.site_id = site_id
        self.message = f"Region with ID: {self.region_id} is associated with a Site with ID: {self.site_id}"
        super().__init__(self.message)  
