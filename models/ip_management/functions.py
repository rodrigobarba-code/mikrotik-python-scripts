class IPAddressesFunctions:
    def __init__(self):  
        pass

    @staticmethod
    def delete_ip_segments(session, ip_data):
        try:
            router_segment_list_p = [str(router_segment.ip_segment_ip) + "/" + str(router_segment.ip_segment_mask) + "@" + str(router_segment.ip_segment_interface) for router_segment in ip_data['ip_list'] if router_segment.fk_router_id == ip_data['router_id']]
            from models.ip_management.models import IPSegment
            ip_segments = session.query(IPSegment).filter(
                IPSegment.fk_router_id == ip_data['router_id']
            ).all()
            for ip_segment in ip_segments:
                if str(ip_segment.ip_segment_ip) + "/" + str(ip_segment.ip_segment_mask) + "@" + str(ip_segment.ip_segment_interface) not in router_segment_list_p:
                    session.delete(ip_segment)
        except Exception as e:  
            print('Error on deleting IP segments: ' + str(e))

    @staticmethod
    def determine_ip_segment_tag(ip_segment_ip: str) -> str:
        try:
            from entities.ip_segment import IPSegmentTag
            from models.ip_management.models import IPSegment

            if ip_segment_ip.startswith("10."):
                return IPSegmentTag.PRIVATE_IP.value
            else:
                return IPSegmentTag.PUBLIC_IP.value
        except Exception as e:  
            raise Exception('Error on determining IP segment tag: ' + str(e))
