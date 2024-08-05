# Description: Sites Entities

# Class for Site Entity
class SiteEntity:
    # Constructor
    def __init__(
        self,
        site_id,  # Site ID
        fk_region_id,  # Foreign Key Region ID
        site_name,  # Site Name
        site_segment  # Site Segment
    ):
        self.site_id = site_id
        self.fk_region_id = fk_region_id
        self.site_name = site_name
        self.site_segment = site_segment
    # Constructor

    # Validate Site Entity
    def validate(self):
        try:
            assert isinstance(self.site_id, int)
            assert isinstance(self.fk_region_id, int)
            assert isinstance(self.site_name, str)
            assert isinstance(self.site_segment, int)
        except AssertionError:
            raise ValueError('Invalid Site Entity')
    # Validate Site Entity
# Class for Site Entity
