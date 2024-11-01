from entities.arp import ARPEntity
from entities.ip_groups import IPGroupsEntity
from models.ip_management.models import IPSegment
from utils.threading_manager import ThreadingManager
from mac_vendor_lookup import MacLookup, BaseMacLookup

class ARPFunctions:
    def __init__(self):  
        pass

    @staticmethod
    def validate_arp_exists(session, arp_ip, arp_mac):
        try:
            from models.router_scan.models import ARP
            arp = session.query(ARP).filter(
                ARP.arp_ip == arp_ip
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
    def validate_incoming_arp(arp_database: tuple, incoming_arp: tuple) -> list:
        """
        Validate incoming ARP data
        :param arp_database:
        :param incoming_arp:
        :return:
        """
        try:
            # Check if the ARP entry is dynamic and does not have a MAC address and is not complete
            if incoming_arp[1][0] == True and incoming_arp[1][1] == False:
                future_table = ['IPGroups', 'blacklist']
            # Check if the ARP entry is dynamic and has a MAC address and is complete
            elif incoming_arp[1][0] == True and incoming_arp[1][1] == True:
                future_table = ['IPGroups', 'authorized']
            else:
                future_table = None

            # Check if the future table is different from the current table
            if future_table:
                # Move the ARP entry to the IP Groups table
                if (arp_database[1][1] == 'ARP') and (future_table[0] == 'IPGroups'):
                    return [False, 'IPGroups', future_table[1]]
                # Move the IP Groups entry to the ARP table
                elif (arp_database[1][1] == 'IPGroups') and (future_table[0] == 'ARP'):
                    return [False, 'ARP', None]
                # If the ARP entry is already in the same table as the future table
                elif (arp_database[1][1] == future_table[0]):
                    return [True, None, None]
            else:
                return [True, None, None]
        except Exception as e:
            print(str(e))
            return [True, None, None]

    @staticmethod
    def find_by_ip_mac_interface(lst: list, ip_mac_interface: tuple):
        """
        Find a tuple in a list of tuples by IP, MAC, and Interface
        :param lst: List of tuples
        :param ip_mac_interface: Tuple with IP, MAC, and Interface
        :return: Tuple with IP, MAC, and Interface
        """
        # For each tuple in the list
        for tup in lst:
            if tup[0] == ip_mac_interface:
                # Return the tuple
                return tup
        return None

    @staticmethod
    def get_mac_vendor(mac: str, operator) -> str:
        """
        Get the MAC vendor from the MAC address of the device
        :param mac: MAC address of the device
        :return: MAC vendor of the device
        """
        try:
            return operator.lookup(mac) if operator.lookup(mac) else 'Unknown'
        except Exception as e:
            return 'Unknown'

    @staticmethod
    def bulk_insert_decision(session, arp_list: list, mac) -> None:
        """
        Decide if the ARP entries need to be inserted on ARP Table or IPGroups Table
        :param arp_list: List of ARP entries
        :param mac: MAC lookup operator
        :param session: Database session
        :return: None
        """
        # Importing here to avoid circular imports
        try:
            from models.router_scan.models import ARP
            from models.ip_management.models import IPGroups

            # Create lists for ARP entries and IPGroup entries
            list_arp, list_ip_groups = [], []

            # Iterate over the ARP entries
            for arp in arp_list:
                # Check if the ARP entry is dynamic and does not have a MAC address and is not complete
                if (arp.arp_is_dynamic is True and arp.arp_is_complete is False) or (arp.arp_is_dynamic is False and arp.arp_is_complete is True):
                    list_ip_groups.append(IPGroupsEntity(
                        ip_group_id=0,
                        fk_ip_segment_id=arp.fk_ip_address_id,
                        ip_group_name='blacklist',
                        ip_group_type='public' if arp.arp_tag == 'Public IP' else 'private',
                        ip_group_alias=arp.arp_alias,
                        ip_group_description='No description',
                        ip_group_ip=arp.arp_ip,
                        ip_group_mask=session.query(IPSegment).filter(
                            IPSegment.ip_segment_id == arp.fk_ip_address_id).first().ip_segment_mask,
                        ip_group_mac=arp.arp_mac,
                        ip_group_mac_vendor=ARPFunctions.get_mac_vendor(arp.arp_mac, mac),
                        ip_group_interface=arp.arp_interface,
                        ip_group_comment='No comment',
                        ip_is_dhcp=arp.arp_is_dhcp,
                        ip_is_dynamic=arp.arp_is_dynamic,
                        ip_is_complete=arp.arp_is_complete,
                        ip_is_disabled=arp.arp_is_disabled,
                        ip_is_published=arp.arp_is_published,
                        ip_duplicity=False,
                        ip_duplicity_indexes=''
                    ))
                # Check if the ARP entry is dynamic and has a MAC address and is complete
                elif arp.arp_is_dynamic is True and arp.arp_is_complete is True:
                    list_ip_groups.append(IPGroupsEntity(
                        ip_group_id=0,
                        fk_ip_segment_id=arp.fk_ip_address_id,
                        ip_group_name='authorized',
                        ip_group_type='public' if arp.arp_tag == 'Public IP' else 'private',
                        ip_group_alias=arp.arp_alias,
                        ip_group_description='No description',
                        ip_group_ip=arp.arp_ip,
                        ip_group_mask=session.query(IPSegment).filter(
                            IPSegment.ip_segment_id == arp.fk_ip_address_id).first().ip_segment_mask,
                        ip_group_mac=arp.arp_mac,
                        ip_group_mac_vendor=ARPFunctions.get_mac_vendor(arp.arp_mac, mac),
                        ip_group_interface=arp.arp_interface,
                        ip_group_comment='No comment',
                        ip_is_dhcp=arp.arp_is_dhcp,
                        ip_is_dynamic=arp.arp_is_dynamic,
                        ip_is_complete=arp.arp_is_complete,
                        ip_is_disabled=arp.arp_is_disabled,
                        ip_is_published=arp.arp_is_published,
                        ip_duplicity=False,
                        ip_duplicity_indexes=''
                    ))
                else:
                    list_arp.append(ARPEntity(
                        arp_id=0,
                        fk_ip_address_id=arp.fk_ip_address_id,
                        arp_ip=arp.arp_ip,
                        arp_mac=arp.arp_mac,
                        arp_interface=arp.arp_interface,
                        arp_is_dhcp=arp.arp_is_dhcp,
                        arp_is_dynamic=arp.arp_is_dynamic,
                        arp_is_complete=arp.arp_is_complete,
                        arp_is_disabled=arp.arp_is_disabled,
                        arp_is_published=arp.arp_is_published,
                        arp_tag=arp.arp_tag,
                        arp_alias=arp.arp_alias
                    ))

            # Insert ARP entries to the database
            if len(list_arp) > 0:
                ThreadingManager().run_thread(ARP.bulk_add_arp, 'w', list_arp)
                print(f'ARP entries inserted: {len(list_arp)}')
            # Insert IPGroup entries to the database
            elif len(list_ip_groups) > 0:
                ThreadingManager().run_thread(IPGroups.bulk_add_ip_groups, 'w', list_ip_groups)
                print(f'IPGroup entries inserted: {len(list_ip_groups)}')
            else:
                print('No ARP entries to insert or move')
        except Exception as e:
            print(str(e))

    @staticmethod
    def arp_bulk_insert_and_validation(session, arp_list: list) -> None:
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

            # Set the cache path for the MAC lookup
            BaseMacLookup.cache_path = "./mac.txt"
            mac = MacLookup()
            mac.update_vendors()
            # from models.router_scan.models import ARPTags

            # Insert ARP entries to the database
            ARPFunctions.bulk_insert_decision(session, arp_list, mac)

            # Create list for ARP entries that needs to move from ARP Table to IPGroups Table
            # Create list for ARP entries that needs to move from IPGroups Table to ARP Table
            # Create list for ARP entries that needs to delete from ARP Table
            arp_to_ip_groups, ip_groups_for_movement = [], []
            ip_groups_to_arp = []

            arps_to_delete = []

            # Create list for ARP entries that are present in the router
            arps_in_database = []

            # Get all ARP entries from the database
            for arp in session.query(ARP.arp_id, ARP.arp_ip, ARP.arp_mac, ARP.arp_interface, ARP.arp_is_dynamic, ARP.arp_is_complete).all():
                arps_in_database.append(((arp.arp_ip, arp.arp_mac, arp.arp_interface), (arp.arp_id, 'ARP', None), (arp.arp_is_dynamic, arp.arp_is_complete)))

            # Get all IPGroup entries from the database
            for ipgroup in session.query(IPGroups.ip_group_id, IPGroups.ip_group_ip, IPGroups.ip_group_mac, IPGroups.ip_group_interface, IPGroups.ip_group_name, IPGroups.ip_is_dynamic, IPGroups.ip_is_complete).all():
                arps_in_database.append(((ipgroup.ip_group_ip, ipgroup.ip_group_mac, ipgroup.ip_group_interface), (ipgroup.ip_group_id, 'IPGroups', ipgroup.ip_group_name), (ipgroup.ip_is_dynamic, ipgroup.ip_is_complete)))

            # Convert the incoming ARP entries from the router to a list of tuples with the format (arp_ip, arp_mac, arp_interface)
            incoming_arp = [
                ((arp.arp_ip, arp.arp_mac, arp.arp_interface), (arp.arp_is_dynamic, arp.arp_is_complete))
                for arp in arp_list
            ]

            # For each Incoming ARP entry from the router
            for arp in arps_in_database:
                # Check if the ARP entry in the database is present in the router

                # Get the ARP entry from incoming ARP list
                incoming_arp_entry = ARPFunctions.find_by_ip_mac_interface(incoming_arp, arp[0])

                if incoming_arp_entry is None: # Delete
                    # Delete
                    arps_to_delete.append(arp[1])
                else: # Move
                    # Validate incoming ARP data
                    arp_decision = ARPFunctions.validate_incoming_arp(arp, incoming_arp_entry)

                    # If it has the same information, don't do anything
                    if not arp_decision[0]:
                        # Move the ARP entry depending on the decision
                        if arp_decision[1] == 'IPGroups':
                            arp_to_ip_groups.append(arp[1][0])
                            ip_groups_for_movement.append(arp_decision[2])
                        elif arp_decision[1] == 'ARP':
                            ip_groups_to_arp.append(arp[1][0])

            # Check if there are ARP entries to move from ARP Table to IPGroups Table
            # Check if there are ARP entries to move from IPGroups Table to ARP Table
            # Check if there are ARP entries to delete from ARP Table
            if arp_to_ip_groups:
                # Move ARP entries to IPGroups
                arp_metadata = [arp_to_ip_groups, ip_groups_for_movement, mac]
                ThreadingManager().run_thread(ARP.bulk_move_arp_to_ip_groups, 'w', arp_metadata)
                print(f'ARP entries moved to IPGroups: {len(arp_to_ip_groups)}')
            elif ip_groups_to_arp:
                # Move IPGroup entries to ARP
                ThreadingManager().run_thread(IPGroups.bulk_move_ip_groups_to_arp, 'w', ip_groups_to_arp)
                print(f'IPGroup entries moved to ARP: {len(ip_groups_to_arp)}')
            elif arps_to_delete:
                # Create lists for ARP entries and IPGroup entries to delete
                list_arp = [item[0] for item in arps_to_delete if item[1] == 'ARP']
                list_ip_groups = [item[0] for item in arps_to_delete if item[1] == 'IPGroups']

                # Validate bulk delete
                # Delete ARP entries from the database
                if list_arp:
                    ThreadingManager().run_thread(ARP.bulk_delete_arps, 'w', list_arp)
                # Delete IPGroup entries from the database
                elif list_ip_groups:
                    ThreadingManager().run_thread(IPGroups.bulk_delete_ip_groups, 'w', list_ip_groups)

                print(f'ARP entries deleted: {len(list_arp)}')
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
