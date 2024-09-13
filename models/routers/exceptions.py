class BaseCustomError(Exception):
    pass  

class RouterError(BaseCustomError):
    def __init__(self, message="An error occurred with the Router Section"):
        self.message = message  
        super().__init__(self.message)  

class RouterAlreadyExists(BaseCustomError):
    def __init__(self, router_id, router_name):
        self.router_id = router_id  
        self.router_name = router_name  
        
        self.message = f"Already exists a router with the name '{self.router_name}', with Router ID: {self.router_id}"
        super().__init__(self.message)  
    
class RouterNotFound(BaseCustomError):
    def __init__(self, router_id):
        self.router_id = router_id  
        
        self.message = f"Router with ID: {self.router_id} not found"
        super().__init__(self.message)

class RouterOnBulkDeleteNotFound(BaseCustomError):
    def __init__(self):
        self.message = f"Some routers on the bulk delete list were not found"
        super().__init__(self.message)
    
class RouterIPAlreadyExists(BaseCustomError):
    def __init__(self, router_id, router_ip):
        self.router_id = router_id  
        self.router_ip = router_ip  
        
        self.message = f"A router with the IP: {self.router_ip} already exists, with Router ID: {self.router_id}"
        super().__init__(self.message)  
    
class RouterMACAlreadyExists(BaseCustomError):
    
    def __init__(self, router_id, router_mac):
        self.router_id = router_id  
        self.router_mac = router_mac  
        
        self.message = f"A router with the MAC: {self.router_mac} already exists, with Router ID: {self.router_id}"
        super().__init__(self.message)  
    
class RouterIPNotValid(BaseCustomError):
    def __init__(self, router_ip):
        self.router_ip = router_ip  
        
        self.message = f"The IP: {self.router_ip} is not a valid IP"
        super().__init__(self.message)  
    
class RouterMACNotValid(BaseCustomError):
    def __init__(self, router_mac):
        self.router_mac = router_mac  
        
        self.message = f"The MAC: {self.router_mac} is not a valid MAC"
        super().__init__(self.message)  
