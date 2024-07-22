class SiteEntity:
    def __init__(self, site_id, fk_region_id, site_name, site_segment):
        self.site_id = site_id
        self.fk_region_id = fk_region_id
        self.site_name = site_name
        self.site_segment = site_segment

    def validate(self):
        try:
            assert isinstance(self.site_id, int)
            assert isinstance(self.fk_region_id, int)
            assert isinstance(self.site_name, str)
            assert isinstance(self.site_segment, str)
        except AssertionError:
            raise ValueError('Invalid Site Entity')
