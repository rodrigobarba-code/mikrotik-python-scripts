# Description: IP Address Entities

# Class for IP Segment Entity
class IPSegmentEntity:
    # Constructor
    def __init__(
        self,
        ip_segment_id,  # IP Segment ID
        fk_router_id,  # FK Router ID
        ip_segment_ip,  # IP Segment IP
        ip_segment_mask,  # IP Segment Mask
        ip_segment_network,  # IP Segment Network
        ip_segment_interface,  # IP Segment Interface
        ip_segment_actual_iface,  # IP Segment Actual Interface
        ip_segment_tag,  # IP Segment Tag
        ip_segment_comment,  # IP Segment Comment
        ip_segment_is_invalid,  # IP Segment Is Invalid
        ip_segment_is_dynamic,  # IP Segment Is Dynamic
        ip_segment_is_disabled  # IP Segment Is Disabled
    ):
        self.ip_segment_id = ip_segment_id
        self.fk_router_id = fk_router_id
        self.ip_segment_ip = ip_segment_ip
        self.ip_segment_mask = ip_segment_mask
        self.ip_segment_network = ip_segment_network
        self.ip_segment_interface = ip_segment_interface
        self.ip_segment_actual_iface = ip_segment_actual_iface
        self.ip_segment_tag = ip_segment_tag
        self.ip_segment_comment = ip_segment_comment
        self.ip_segment_is_invalid = ip_segment_is_invalid
        self.ip_segment_is_dynamic = ip_segment_is_dynamic
        self.ip_segment_is_disabled = ip_segment_is_disabled
    # Constructor

    # Validate IP Segment Entity
    def validate_ip_segment(self):
        try:
            # Check for each attribute to be valid
            assert isinstance(self.ip_segment_id, int)  # Verify if IP Segment ID is an Integer or None
            assert isinstance(self.fk_router_id, int)  # Verify if FK Router ID is an Integer
            assert isinstance(self.ip_segment_ip, str)  # Verify if IP Segment IP is a String
            assert isinstance(self.ip_segment_mask, str)  # Verify if IP Segment Mask is a String
            assert isinstance(self.ip_segment_network, str)  # Verify if IP Segment Network is a String
            assert isinstance(self.ip_segment_interface, str)  # Verify if IP Segment Interface is a String
            assert isinstance(self.ip_segment_actual_iface, str)  # Verify if IP Segment Actual Interface is a String
            assert isinstance(self.ip_segment_comment, str)  # Verify if IP Segment Comment is a String
            assert isinstance(self.ip_segment_is_invalid, bool)  # Verify if IP Segment Is Invalid is a Boolean
            assert isinstance(self.ip_segment_is_dynamic, bool)  # Verify if IP Segment Is Dynamic is a Boolean
            assert isinstance(self.ip_segment_is_disabled, bool)  # Verify if IP Segment Is Disabled is a Boolean
            # Check for each attribute to be valid
        except AssertionError:
            raise ValueError('Invalid IP Segment Entity')  # Raise Value Error
    # Validate IP Segment Entity
# Class for IP Segment Entity
