import json
from .. import SessionLocal
from collections import Counter

from entities.arp import ARPTag
from models.ip_management.models import IPSegment

class ARPFunctions:
    def __init__(self):  
        pass

    @staticmethod
    def validate_arp_exists(arp_ip, arp_mac):
        try:
            from models.router_scan.models import ARP
            arp = ARP.query.filter(
                ARP.arp_ip == arp_ip,  
                ARP.arp_mac == arp_mac  
            ).first()
            if arp:
                if arp_ip != arp.arp_ip and arp_mac != arp.arp_mac:
                    return True
                return False  
            else:  
                return True
        except Exception as e:  
            print(str(e))  

    @staticmethod
    def delete_arps(router_arp_list, fk_router_id, model):
        session = SessionLocal()  
        try:
            router_arp_list_p = [str(router_arp.arp_ip) + "@" + str(router_arp.arp_mac) for router_arp in router_arp_list]
            from models.router_scan.models import ARP
            arps = session.query(IPSegment, ARP).join(ARP, IPSegment.ip_segment_id == ARP.fk_ip_address_id).filter(
                IPSegment.fk_router_id == fk_router_id  
            ).all()
            for ip, arp in arps:
                model.delete_arp_tags(arp.arp_id)
                if str(arp.arp_ip) + "@" + str(arp.arp_mac) not in router_arp_list_p:
                    session.delete(arp)  
        except Exception as e:  
            print("Error in delete_arps: " + str(e))  

    @staticmethod
    def detect_ip_duplicated():
        session = SessionLocal()  
        try:
            from models.router_scan.models import ARP
            arps = ARP.query.with_entities(ARP.arp_id, ARP.arp_ip).all()
            arp_ip_count = Counter([arp.arp_ip for arp in arps])
            for item, count in arp_ip_count.items():
                if count > 1:
                    for arp in arps:
                        if arp.arp_ip == item:
                            array = json.loads(arp.arp_tag)
                            array.append(ARPTag.IP_ADDRESS_DUPLICATED)  
                            arp.arp_tag = json.dumps(array)
            session.commit()  
        except Exception as e:  
            print(str(e))  

    @staticmethod
    def assign_alias(arp_ip: str, queue_list: dict) -> str:
        try:
            from models.router_scan.models import ARP
            for key, value in queue_list.items():
                if arp_ip == key:
                    return str(value)  
            else:
                return str("")
        except Exception as e:
            print(str(e))  
