from utils.threading_manager import ThreadingManager


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
    async def get_mac_vendor(mac: str, operator) -> str:
        """
        Get the MAC vendor from the MAC address of the device
        :param mac: MAC address of the device
        :return: MAC vendor of the device
        """
        try:
            return await operator.lookup(mac) if await operator.lookup(mac) else 'Unknown'
        except Exception as e:
            return 'Unknown'

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
    def determine_arp_name(dynamic: bool, complete: bool, mac_address: str) -> str:
        try:
            if dynamic and complete and mac_address != '':
                return 'authorized'
            elif dynamic and complete and mac_address == '':
                return 'blacklist'
            elif dynamic and not complete:
                return 'blacklist'
            else:
                return 'blacklist'
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
    def determine_arp_mask(session, ip_segment_id_x: int) -> str:
        try:
            from models.ip_management.models import IPSegment
            ip_segment = session.query(IPSegment).filter_by(ip_segment_id=ip_segment_id_x).first()
            if ip_segment:
                return '/' + ip_segment.ip_segment_mask
            else:
                return '/24'
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

    @staticmethod
    def validate_ip_group_exists(session, ip_group_ip: str, ip_group_interface: str) -> bool:
        try:
            from models.ip_management.models import IPGroups
            ip_group = session.query(IPGroups).filter(
                IPGroups.ip_group_ip == ip_group_ip,
                IPGroups.ip_group_interface == ip_group_interface
            ).first()
            return True if ip_group else False
        except Exception as e:
            print(str(e))

    @staticmethod
    def validate_ip_group_table_integrity(session, ip_group_ip: str, ip_group_interface: str, incoming_ip_group_list: list) -> bool:
        try:
            from models.ip_management.models import IPGroups
            ip_group = session.query(IPGroups).filter(
                IPGroups.ip_group_ip == ip_group_ip,
                IPGroups.ip_group_interface == ip_group_interface
            ).first()
            if ip_group:
                if ip_group_ip in incoming_ip_group_list:
                    return True
                else:
                    return False
            else:
                return True
        except Exception as e:
            print(str(e))

    @staticmethod
    def place_ip_group_on_table(session, incoming_ip_group_list: list) -> tuple:
        try:
            # Import the IPGroups model
            from models.ip_management.models import IPGroups

            # Create a list of IPs for the incoming IP Groups
            incoming_ip_list = [ip_group.ip_group_ip for ip_group in incoming_ip_group_list]

            # Variables to store the insert, update, and delete operations
            inserted, updated, deleted = 0, 0, 0

            # Create list to store insert and update operations
            insert_list, update_list, delete_list = [], [], []

            # Iterate over the incoming IP Groups
            for i_ip_group in incoming_ip_group_list:
                # Create IP Group object
                ip_group = IPGroups(
                    ip_group_id=i_ip_group.ip_group_id,
                    fk_ip_segment_id=i_ip_group.fk_ip_segment_id,
                    ip_group_name=i_ip_group.ip_group_name,
                    ip_group_type=i_ip_group.ip_group_type,
                    ip_group_alias=i_ip_group.ip_group_alias,
                    ip_group_description=i_ip_group.ip_group_description,
                    ip_group_ip=i_ip_group.ip_group_ip,
                    ip_group_mask=i_ip_group.ip_group_mask,
                    ip_group_mac=i_ip_group.ip_group_mac,
                    ip_group_mac_vendor=i_ip_group.ip_group_mac_vendor,
                    ip_group_interface=i_ip_group.ip_group_interface,
                    ip_group_comment=i_ip_group.ip_group_comment,
                    ip_is_dhcp=i_ip_group.ip_is_dhcp,
                    ip_is_dynamic=i_ip_group.ip_is_dynamic,
                    ip_is_complete=i_ip_group.ip_is_complete,
                    ip_is_disabled=i_ip_group.ip_is_disabled,
                    ip_is_published=i_ip_group.ip_is_published,
                    ip_duplicity=i_ip_group.ip_duplicity,
                    ip_duplicity_indexes=i_ip_group.ip_duplicity_indexes
                )

                # Check if the IP Group is already in the database
                if ARPFunctions.validate_ip_group_exists(session, ip_group.ip_group_ip, ip_group.ip_group_interface):
                    # Check if the IP Group is in the incoming IP Group list
                    if ARPFunctions.validate_ip_group_table_integrity(session, ip_group.ip_group_ip, ip_group.ip_group_interface, incoming_ip_list):
                        # Update the IP Group
                        update_list.append(ip_group)
                    else:
                        # Delete the IP Group
                        delete_list.append(ip_group)
                else:
                    # Insert the IP Group
                    insert_list.append(ip_group)

            # Insert the IP Groups
            if insert_list:
                inserted = len(insert_list)
                ThreadingManager().run_thread(IPGroups.bulk_add_ip_groups, 'w', insert_list)

            # Update the IP Groups
            if update_list:
                updated = len(update_list)
                ThreadingManager().run_thread(IPGroups.bulk_update_ip_groups, 'w', update_list)

            # Delete the IP Groups
            if delete_list:
                deleted = len(delete_list)
                ThreadingManager().run_thread(IPGroups.bulk_delete_ip_groups, 'w', delete_list)

            # Return the number of inserted, updated, and deleted IP Groups
            return inserted, updated, deleted
        except Exception as e:
            print(str(e))