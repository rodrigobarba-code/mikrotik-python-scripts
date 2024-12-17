class IPGroupsTagsEntity:
    def __init__(
        self,
        ip_group_tag_id: int,
        ip_group_tag_name: str,
        ip_group_tag_color: str = None,
        ip_group_tag_text_color: str = None,
        ip_group_tag_description: str = None,
    ):
        self.ip_group_tag_id = ip_group_tag_id
        self.ip_group_tag_name = ip_group_tag_name
        self.ip_group_tag_color = ip_group_tag_color
        self.ip_group_tag_text_color = ip_group_tag_text_color
        self.ip_group_tag_description = ip_group_tag_description

    def validate_ip_group_tag(self):
        try:
            assert isinstance(self.ip_group_tag_id, int)
            assert isinstance(self.ip_group_tag_name, str)
            assert isinstance(self.ip_group_tag_color, (str, type(None)))
            assert isinstance(self.ip_group_tag_text_color, (str, type(None)))
            assert isinstance(self.ip_group_tag_description, (str, type(None)))
        except AssertionError:
            raise ValueError('Invalid IP Group Tag data')

class IPGroupsEntity:
    def __init__(
        self,
        ip_group_id: int,
        fk_ip_segment_id: int = None,
        ip_group_name: str = 'connected',
        ip_group_type: str = 'public',
        ip_group_alias: str = None,
        ip_group_description: str = None,
        ip_group_ip: str = None,
        ip_group_mask: str = None,
        ip_group_mac: str = None,
        ip_group_mac_vendor: str = 'Unknown',
        ip_group_interface: str = None,
        ip_group_comment: str = None,
        ip_is_dhcp: bool = False,
        ip_is_dynamic: bool = False,
        ip_is_complete: bool = False,
        ip_is_disabled: bool = False,
        ip_is_published: bool = False,
        ip_duplicity: bool = False,
        ip_duplicity_indexes: str = '',
    ):
        self.ip_group_id = ip_group_id
        self.fk_ip_segment_id = fk_ip_segment_id
        self.ip_group_name = ip_group_name
        self.ip_group_type = ip_group_type
        self.ip_group_alias = ip_group_alias
        self.ip_group_description = ip_group_description
        self.ip_group_ip = ip_group_ip
        self.ip_group_mask = ip_group_mask
        self.ip_group_mac = ip_group_mac
        self.ip_group_mac_vendor = ip_group_mac_vendor
        self.ip_group_interface = ip_group_interface
        self.ip_group_comment = ip_group_comment
        self.ip_is_dhcp = ip_is_dhcp
        self.ip_is_dynamic = ip_is_dynamic
        self.ip_is_complete = ip_is_complete
        self.ip_is_disabled = ip_is_disabled
        self.ip_is_published = ip_is_published
        self.ip_duplicity = ip_duplicity
        self.ip_duplicity_indexes = ip_duplicity_indexes

    def validate_ip_group(self):
        try:
            assert isinstance(self.ip_group_id, int)
            assert isinstance(self.fk_ip_segment_id, int)
            assert isinstance(self.ip_group_alias, (str, type(None)))
            assert isinstance(self.ip_group_description, (str, type(None)))
            assert isinstance(self.ip_group_ip, (str, type(None)))
            assert isinstance(self.ip_group_mask, (str, type(None)))
            assert isinstance(self.ip_group_mac, (str, type(None)))
            assert isinstance(self.ip_group_mac_vendor, str)
            assert isinstance(self.ip_group_interface, (str, type(None)))
            assert isinstance(self.ip_group_comment, (str, type(None)))
            assert isinstance(self.ip_is_dhcp, bool)
            assert isinstance(self.ip_is_dynamic, bool)
            assert isinstance(self.ip_is_complete, bool)
            assert isinstance(self.ip_is_disabled, bool)
            assert isinstance(self.ip_is_published, bool)
            assert isinstance(self.ip_duplicity, bool)
            assert isinstance(self.ip_duplicity_indexes, str)
        except (AssertionError, ValueError):
            raise ValueError('Invalid IP Group data')
