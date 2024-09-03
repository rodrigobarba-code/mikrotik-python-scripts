# Description: Scan Entities

# Class for ARP Tags
class ARPTag:
    # Constructor
    def __init__(
        self,
        arp_tag_id,  # ARP Tag ID
        fk_arp_id,  # FK ARP ID
        arp_tag_value,  # ARP Tag Value
    ):
        self.arp_tag_id = arp_tag_id
        self.fk_arp_id = fk_arp_id
        self.arp_tag_value = arp_tag_value
    # Constructor

    # Validate ARP Tag
    def validate_arp_tag(self):
        try:
            assert isinstance(self.arp_tag_id, int)  # Verify if ARP Tag ID is an Integer
            assert isinstance(self.fk_arp_id, int)  # Verify if FK ARP ID is an Integer
            assert isinstance(self.arp_tag_value, str)  # Verify if ARP Tag Value is a String
        except AssertionError:  # If any of the above assertions fail
            raise ValueError('Invalid ARP Tag')  # Raise a ValueError
    # Validate ARP Tag

    # Get Tags
    @staticmethod
    def get_tags():
        return {
            'PUBLIC_IP': 'Public IP',  # Public IP
            'PRIVATE_IP': 'Private IP',  # Private IP
            'INTERNAL_CONNECTION': 'Internal Connection',  # Internal Connection
            'EXTERNAL_CONNECTION': 'External Connection',  # External Connection
            'DUPLICATED_IP': 'Duplicated IP',  # Duplicated IP
        }
    # Get Tags
# Class for ARP Tags

# Class for ARP Entity
class ARPEntity:
    # Constructor
    def __init__(
        self,
        arp_id,  # ARP ID
        fk_ip_address_id,  # FK IP Address ID
        arp_ip,  # ARP IP
        arp_mac,  # ARP MAC
        arp_alias,  # ARP Alias
        arp_interface,  # ARP Interface
        arp_is_dhcp,  # ARP DHCP
        arp_is_invalid,  # ARP Invalid
        arp_is_dynamic,  # ARP Dynamic
        arp_is_complete,  # ARP Complete
        arp_is_disabled,  # ARP Disabled
        arp_is_published,  # ARP Published
    ):
        self.arp_id = arp_id
        self.fk_ip_address_id = fk_ip_address_id
        self.arp_ip = arp_ip
        self.arp_mac = arp_mac
        self.arp_alias = arp_alias
        self.arp_interface = arp_interface
        self.arp_is_dhcp = arp_is_dhcp
        self.arp_is_invalid = arp_is_invalid
        self.arp_is_dynamic = arp_is_dynamic
        self.arp_is_complete = arp_is_complete
        self.arp_is_disabled = arp_is_disabled
        self.arp_is_published = arp_is_published
    # Constructor

    # Validate ARP Entity
    def validate_arp(self):
        try:
            # Check for each attribute to be valid
            assert isinstance(self.arp_id, int)  # Verify if ARP ID is an Integer
            assert isinstance(self.fk_ip_address_id, int)  # Verify if FK IP Address ID is an Integer
            assert isinstance(self.arp_ip, str)  # Verify if ARP IP is a String
            assert isinstance(self.arp_mac, str)  # Verify if ARP MAC is a String
            assert isinstance(self.arp_interface, str)  # Verify if ARP Interface is a String
            assert isinstance(self.arp_is_dhcp, bool)  # Verify if ARP DHCP is a Boolean
            assert isinstance(self.arp_is_invalid, bool)  # Verify if ARP Invalid is a Boolean
            assert isinstance(self.arp_is_dynamic, bool)  # Verify if ARP Dynamic is a Boolean
            assert isinstance(self.arp_is_complete, bool)  # Verify if ARP Complete is a Boolean
            assert isinstance(self.arp_is_disabled, bool)  # Verify if ARP Disabled is a Boolean
            assert isinstance(self.arp_is_published, bool)  # Verify if ARP Published is a Boolean
            # Check for each attribute to be valid
        except AssertionError:
            raise ValueError('Invalid ARP Entity')
    # Validate ARP Entity
# Class for ARP Entity
