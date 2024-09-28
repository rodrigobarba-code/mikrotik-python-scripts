import ipaddress

class FindIPSegment:
    def __init__(
        self,
        session=None,
    ):
        self.session = session

    def get_session(self):
        return self.session

    def set_session(self, session):
        self.session = session

    @staticmethod
    def find(ip_segments, arp_ip) -> list:
        try:
            ip = ipaddress.ip_address(arp_ip)

            ip_segments_set = [[segment.ip_segment_id, segment.ip_segment_ip, segment.ip_segment_ip + "/" + segment.ip_segment_mask] for segment in ip_segments]

            for ip_network in ip_segments_set:
                network = ipaddress.ip_network(ip_network[2], strict=False)
                if ip in network:
                    return [True, int(ip_network[0])]
            else:
                return [False, None]
        except Exception as e:
            raise str("An error occurred while finding the IP Segment: " + str(e))
