from .. import SessionLocal

class IPAddressesFunctions:
    def __init__(self):  
        pass  

    @staticmethod
    def validate_ip_segment_exists(ip_segment_ip, ip_segment_mask, ip_segment_interface):
        try:
            from models.ip_management.models import IPSegment
            ip_segment = IPSegment.query.filter(
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
    def delete_ip_segments(router_segment_list, fk_router_id):
        session = SessionLocal()  
        try:
            router_segment_list_p = [str(router_segment.ip_segment_ip) + "/" + str(router_segment.ip_segment_mask) + "@" + str(router_segment.ip_segment_interface) for router_segment in router_segment_list if router_segment.fk_router_id == fk_router_id]
            from models.ip_management.models import IPSegment
            ip_segments = IPSegment.query.filter(
                IPSegment.fk_router_id == fk_router_id  
            ).all()
            for ip_segment in ip_segments:
                if str(ip_segment.ip_segment_ip) + "/" + str(ip_segment.ip_segment_mask) + "@" + str(ip_segment.ip_segment_interface) not in router_segment_list_p:
                    session.delete(ip_segment)
            session.commit()  
        except Exception as e:  
            session.rollback()  
            print(str(e))  

    @staticmethod
    def determine_ip_segment_tag(ip_segment_ip):
        try:
            from entities.ip_segment import IPSegmentTag
            from models.ip_management.models import IPSegment

            if ip_segment_ip.startswith("10."):
                return IPSegmentTag.PRIVATE_IP  
            else:
                return IPSegmentTag.PUBLIC_IP
            
        except Exception as e:  
            print(str(e))  
