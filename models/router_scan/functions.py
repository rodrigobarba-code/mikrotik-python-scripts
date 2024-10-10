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
            from models.router_scan.models import ARPTags

            # Create a list of tuples with the ARP entries obtained from the router
            r_arp_list_real = [
                (arp.arp_ip, arp.arp_mac)
                for arp in router_metadata['arp_region_list']
            ]

            # Create a list of ARP entries from the database
            r_arp_list_db = [
                arp for arp in session.query(IPSegment, ARP).join(ARP, IPSegment.ip_segment_id == ARP.fk_ip_address_id).filter(
                    IPSegment.fk_router_id == router_metadata['router_id']
                ).all()
            ]

            # Create a list for all ARP entries that need to be deleted
            arps_to_delete = []

            # Validate if the ARP entry exists in the database but not in the router
            if r_arp_list_real:
                for r_arp in r_arp_list_db:
                    # If the ARP entry exists in the database but not in the router, add it to the list of ARP entries to delete
                    if (r_arp[1].arp_ip, r_arp[1].arp_mac) not in r_arp_list_real:
                        ThreadingManager().run_thread(ARPTags.delete_arp_tags, 'w', r_arp[1].arp_id)
                        arps_to_delete.append(r_arp[1])

            # If there are ARP entries to delete, delete them
            if arps_to_delete:
                # Create a list of ARP IDs to delete
                arps_ids_to_delete = [arp.arp_id for arp in arps_to_delete]

                # Delete ARP entries from the database
                session.query(ARP).filter(ARP.arp_id.in_(arps_ids_to_delete)).delete(synchronize_session='fetch')

                print("Deleted ARP entries: " + str(len(arps_ids_to_delete)))
            else:
                print("No ARP entries to delete")
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
    def validate_bulk_delete(session, model, arp_ids):
        try:
            from models.router_scan.models import ARP
            if not session.query(model).filter(model.arp_id.in_(arp_ids)).all():
                raise Exception('ARP not found')
            return True
        except Exception as e:
            print(str(e))
