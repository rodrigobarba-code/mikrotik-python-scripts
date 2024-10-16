from entities.arp import ARPEntity
from models.ip_management.models import IPSegment
from utils.threading_manager import ThreadingManager

class ARPFunctions:
    def __init__(self):  
        pass

    @staticmethod
    def validate_arp_exists(session, arp_ip, arp_mac):
        try:
            from models.router_scan.models import ARP
            arp = session.query(ARP).filter(
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
    def validate_incoming_arp(arp_database: ARPEntity) -> tuple:
        try:
            """
            Validate incoming ARP data
            :param arp_data: ARP data
            :return: Tuple
            """
            if bool(arp_database.arp_is_dynamic) is True and bool(arp_database.arp_is_complete) is True:
                return (True, None)
        except Exception as e:
            return (False, str(e))

    @staticmethod
    def delete_arps(session, router_metadata: dict) -> None:
        """
        Delete ARP entries from the database that are not present in the router
        :param session: Database session
        :param router_metadata: Router metadata
        :return: None
        """
        try:
            # Importing here to avoid circular imports
            from models.router_scan.models import ARP
            from models.ip_management.models import IPGroups
            # from models.router_scan.models import ARPTags

            # Create list for ARP entries that needs to move from ARP Table to IPGroups Table
            # Create list for ARP entries that needs to move from IPGroups Table to ARP Table
            # Create list for ARP entries that needs to delete from ARP Table
            arp_to_ipgroups = []
            ipgroups_to_arp = []

            arps_to_delete = []

            # Create list for ARP entries that are present in the router
            arps_in_database = []

            # Get all ARP entries from the database
            for arp in session.query(ARP.arp_id, ARP.arp_ip, ARP.arp_mac, ARP.arp_interface).all():
                arps_in_database.append((arp.arp_ip, arp.arp_mac, arp.arp_interface, arp.arp_id, 'ARP', None))

            # Get all IPGroup entries from the database
            for ipgroup in session.query(IPGroups.ip_group_id, IPGroups.ip_group_ip, IPGroups.ip_group_mac, IPGroups.ip_group_interface, IPGroups.ip_group_name).all():
                arps_in_database.append((ipgroup.ip_group_id, ipgroup.ip_group_ip, ipgroup.ip_group_mac, ipgroup.ip_group_interface, 'IPGroups', ipgroup.ip_group_name))

            # For each Incoming ARP entry from the router
            for arp in router_metadata['arp_region_list']:
                pass

        except Exception as e:  
            print(str("Error in delete_arps: " + str(e)))

    """
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
    """

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

    @staticmethod
    def determine_arp_tag(arp_ip: str) -> str:
        try:
            if arp_ip.startswith("10."):
                return 'Private IP'
            else:
                return 'Public IP'
        except Exception as e:
            print(str(e))

    @staticmethod
    def validate_bulk_delete(session, model, arp_ids):
        try:
            from models.router_scan.models import ARP
            if not session.query(model).filter(model.arp_id.in_(arp_ids)).all():
                raise Exception('ARP not found')
            return True
        except Exception as e:
            print(str(e))
