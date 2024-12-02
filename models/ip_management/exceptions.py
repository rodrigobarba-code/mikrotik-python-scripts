class BaseCustomError(Exception):
    pass  

class IPSegmentError(BaseCustomError):
    def __init__(self, message="An error occurred with the IP Segment Blueprint."):
        self.message = message  
        super().__init__(self.message)  
    
class IPSegmentNotFound(IPSegmentError):
    def __init__(self, ip_segment_id, message="The IP Segment was not found."):
        self.ip_segment_id = ip_segment_id
        self.message = message
        super().__init__(self.message)  
    
class IPSegmentAlreadyExists(IPSegmentError):
    def __init__(self, message="The IP Segment already exists."):
        self.message = message  
        super().__init__(self.message)  
