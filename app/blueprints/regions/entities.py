# Description: Region Entities

# Class for Region Entity
class RegionEntity:
    # Constructor
    def __init__(
        self,
        region_id,  # Region ID
        region_name  # Region Name
    ):
        self.region_id = region_id
        self.region_name = region_name
    # Constructor

    # Validate Region Entity
    def validate(self):
        try:
            # Check for each attribute to be valid
            assert isinstance(self.region_id, int)  # Verify if Region ID is an Integer
            assert isinstance(self.region_name, str)  # Verify if Region Name is a String
            # Check for each attribute to be valid
        except AssertionError:
            raise ValueError('Invalid Region Entity')  # Raise ValueError if Assertion Error
    # Validate Region Entity
# Class for Region Entity
