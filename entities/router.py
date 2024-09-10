# Description: Router Entities

# Class for Router Entity
class RouterEntity:
    # Constructor
    def __init__(
        self,
        router_id,  # Router ID
        router_name,  # Router Name
        router_description,  # Router Description
        router_brand,  # Router Brand
        router_model,  # Router Model
        fk_site_id,  # Foreign Key Site ID
        router_ip,  # Router IP
        router_mac,  # Router MAC
        router_username,  # Router Username
        router_password,  # Router Password
        allow_scan  # Allow Scan
    ):
        self.router_id = router_id
        self.router_name = router_name
        self.router_description = router_description
        self.router_brand = router_brand
        self.router_model = router_model
        self.fk_site_id = fk_site_id
        self.router_ip = router_ip
        self.router_mac = router_mac
        self.router_username = router_username
        self.router_password = router_password
        self.allow_scan = allow_scan
    # Constructor

    # Validate Router Entity
    def validate(self):
        try:
            # Check for each attribute to be valid
            assert isinstance(self.router_id, int)  # Verify if Router ID is an Integer
            assert isinstance(self.router_name, str)  # Verify if Router Name is a String
            assert isinstance(self.router_description, str)  # Verify if Router Description is a String
            assert isinstance(self.router_brand, str)  # Verify if Router Brand is a String
            assert isinstance(self.router_model, str)  # Verify if Router Model is a String
            assert isinstance(self.fk_site_id, int)  # Verify if Foreign Key Site ID is an Integer
            assert isinstance(self.router_ip, str)  # Verify if Router IP is a String
            assert isinstance(self.router_mac, str)  # Verify if Router MAC is a String
            assert isinstance(self.router_username, str)  # Verify if Router Username is a String
            assert isinstance(self.router_password, str)  # Verify if Router Password is a String
            assert isinstance(self.allow_scan, int)  # Verify if Allow Scan is an Integer
            # Check for each attribute to be valid
        except AssertionError:
            raise ValueError('Invalid Router Entity')
    # Validate Router Entity
# Class for Router Entity
