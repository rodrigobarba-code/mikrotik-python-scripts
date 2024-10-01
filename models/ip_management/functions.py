class IPAddressesFunctions:
    def __init__(self):  
        pass

    @staticmethod
    def validate_ip_segment_exists(session, ip_segment_ip, ip_segment_mask, ip_segment_interface):
        try:
            from models.ip_management.models import IPSegment
            ip_segment = session.query(IPSegment).filter(
                IPSegment.ip_segment_ip == ip_segment_ip,
                IPSegment.ip_segment_mask == ip_segment_mask,
                IPSegment.ip_segment_interface == ip_segment_interface
            ).first()
            if ip_segment:
                if ip_segment_ip != ip_segment.ip_segment_ip and ip_segment_mask != ip_segment.ip_segment_mask and ip_segment_interface != ip_segment.ip_segment_interface:
                    return True
                return False
            else:
                return True
        except Exception as e:
            print(str(e))

    @staticmethod
    def delete_ip_segments(session, ip_data):
        try:
            from sqlalchemy import delete
            from models.ip_management.models import IPSegment

            r_segment_list_real = [
                (router_segment.ip_segment_ip,
                 router_segment.ip_segment_mask,
                 router_segment.ip_segment_interface)
                for router_segment in ip_data['ip_list']
                if router_segment.fk_router_id == ip_data['router_id']
            ]

            r_segments_list_db = [
                ip_segment for ip_segment in session.query(IPSegment).filter(
                    IPSegment.fk_router_id == ip_data['router_id']
                ).all()
            ]

            segments_to_delete = []

            if r_segment_list_real:
                for r_segment in r_segments_list_db:
                    if (r_segment.ip_segment_ip, r_segment.ip_segment_mask, r_segment.ip_segment_interface) not in r_segment_list_real:
                        segments_to_delete.append(r_segment)

            if segments_to_delete:
                session.delete(segments_to_delete)
                print('Deleted IP segments: ' + str(segments_to_delete))
            else:
                print('No segments to delete.')
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
