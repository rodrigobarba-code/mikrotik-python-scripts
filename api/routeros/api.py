import asyncio

import ros_api

from utils.threading_manager import ThreadingManager

from entities.arp import ARPEntity
# from models.router_scan.models import ARPTags
from models.router_scan.functions import ARPFunctions

from entities.ip_segment import IPSegmentEntity
from models.ip_management.models import IPSegment
from models.ip_management.functions import IPAddressesFunctions

from api.routeros.modules.FindIPSegment import FindIPSegment
from api.routeros.modules.GetAllowedRouters import GetAllowedRouters


class RouterAPI:
    POSSIBLE_SCAN_STATUS = ['IDLE', 'IN PROGRESS']

    router = None
    credentials = None
    scan_status = None

    def __init__(
            self,
            host,
            user,
            password
    ):
        self.router = None
        self.credentials = {
            'host': host,
            'user': user,
            'password': password
        }

    @staticmethod
    def get_scan_status():
        return RouterAPI.scan_status

    def set_scan_status(self, status):
        self.scan_status = {'status': status}

    def get_credentials(self):
        return self.credentials

    def set_credentials(
            self,
            host=None,
            user=None,
            password=None
    ):
        self.credentials = {
            'host': host,
            'user': user,
            'password': password
        }

    def get_api(self):
        return self.router

    def set_api(self):
        self.router = ros_api.Api(
            self.credentials['host'],
            self.credentials['user'],
            self.credentials['password'],
            port=7372,
            use_ssl=True
        )

    @staticmethod
    def retrieve_data(router, command) -> dict:
        return router.talk(command)

    @staticmethod
    def communicate_data(router, command: list[str]) -> dict:
        try:
            return router.communicate(command)
        except Exception as e:
            print(str('Error: communicate_data: ' + str(e)))

    def verify_router_connection(router) -> bool:
        try:
            router.talk('/system/resource/print')
            return True
        except (Exception, asyncio.TimeoutError) as e:
            raise e

    @staticmethod
    async def get_ip_data() -> list:
        """
        Get IP segments from all available routers
        :return: List of IP segments
        """

        try:
            # List of IP segments
            ip_list = []

            # Get a list of all allowed routers
            routers = ThreadingManager().run_thread(GetAllowedRouters.get, 'r')

            # Iterate through all available routers
            for router in routers:
                # Create an instance of the RouterAPI class
                router_api_instance = RouterAPI(
                    router['ip'],
                    router['username'],
                    router['password']
                )

                # Set the API connection
                router_api_instance.set_api()

                # Get the IP Address data from the router
                ip_data = RouterAPI.retrieve_data(router_api_instance.get_api(), '/ip/address/print')

                # Iterate through all IP segments for that one router
                for ip in ip_data:
                    # Check if IP segment data field has a comment, if not set it to None in String format
                    comment = "None"
                    if 'comment' in ip:
                        comment = ip['comment']

                    # Split the IP address and the mask
                    ip_tmp = ip['address'].split('/')

                    # Create an instance of the IPSegmentEntity class with the data
                    ip_obj = IPSegmentEntity(
                        ip_segment_id=int(),
                        fk_router_id=router['id'],
                        ip_segment_ip=ip_tmp[0],
                        ip_segment_mask=ip_tmp[1],
                        ip_segment_network=ip['network'],
                        ip_segment_interface=ip['interface'],
                        ip_segment_actual_iface=ip['actual-interface'],
                        ip_segment_tag=IPAddressesFunctions.determine_ip_segment_tag(ip_tmp[0]),
                        # Determine the tag of the IP segment
                        ip_segment_comment=comment,
                        ip_segment_is_invalid=True if ip['invalid'] == 'true' else False,
                        ip_segment_is_dynamic=True if ip['dynamic'] == 'true' else False,
                        ip_segment_is_disabled=True if ip['disabled'] == 'true' else False
                    )

                    # Validate if the IP segment datatype is correct
                    ip_obj.validate_ip_segment()

                    # Concatenate the IP segment to the list
                    ip_list.append(ip_obj)

                # Create a dictionary with the IP list and the router ID
                ip_data = {'ip_list': ip_list, 'router_id': router['id']}

                # Delete all IP segments from the database that are in database but not in the router
                ThreadingManager().run_thread(IPAddressesFunctions.delete_ip_segments, 'w', ip_data)
            return ip_list
        except Exception as e:
            print(str('Error: get_ip_data: ' + str(e)))

    @staticmethod
    async def add_ip_data(ip_list: list[IPSegmentEntity]) -> None:
        """
        Add available IP segments to the database
        :param ip_list: List of IP segments
        :return: None
        """

        try:
            # Validate all IP segments
            for ip in ip_list:
                ip.validate_ip_segment()

            # Add all IP segments to the database in bulk
            ThreadingManager().run_thread(IPSegment.bulk_add_ip_segments, 'w', ip_list)
        except Exception as e:
            print(str('Error: add_ip_data: ' + str(e)))

    @staticmethod
    async def get_arp_data() -> list:
        """
        Get ARP data from all available routers
        :return: List of ARP data
        """

        try:
            # List of ARP data
            arp_list = []

            # Get a list of all allowed routers
            routers = ThreadingManager().run_thread(GetAllowedRouters.get, 'r')

            # Iterate through all available routers
            for router in routers:
                # Create an instance of the RouterAPI class
                router_api_instance = RouterAPI(
                    router['ip'],
                    router['username'],
                    router['password']
                )

                # Set the API connection
                router_api_instance.set_api()

                # Create a list of ARP data for that one router
                arp_region_list = []

                # Get the IP segments by router ID
                ip_segments_by_router = ThreadingManager().run_thread(
                    IPSegment.get_ip_segments_by_router_id,
                    'rx',
                    router['id']
                )

                # Get the ARP data from the router
                arp_data = RouterAPI.retrieve_data(router_api_instance.get_api(), '/ip/arp/print')

                # Obtain the queue data from the router to assign aliases to the ARP data
                queue_dict = {}
                queue_data = RouterAPI.retrieve_data(router_api_instance.get_api(), '/queue/simple/print')
                for queue in queue_data:
                    name = queue['name']
                    ip = queue['target'].split('/')[0]
                    queue_dict[ip] = name

                # Iterate through all ARP data for that one router
                for arp in arp_data:
                    # Find the IP segment by the ARP IP address
                    ip_segment = FindIPSegment.find(ip_segments_by_router, arp['address'])

                    # If there is a match, create an instance of the ARPEntity class with the data
                    if ip_segment[0] is True:
                        # Create an instance of the ARPEntity class with the data
                        arp_obj = ARPEntity(
                            arp_id=int(),
                            fk_ip_address_id=int(ip_segment[1]),
                            arp_ip=arp['address'],
                            arp_mac="" if 'mac-address' not in arp else arp['mac-address'],
                            arp_alias=ARPFunctions.assign_alias(str(arp['address']), queue_dict),
                            arp_tag=ARPFunctions.determine_arp_tag(str(arp['address'])),
                            arp_interface=arp['interface'],
                            arp_is_dhcp=True if arp['dynamic'] == 'true' else False,
                            arp_is_invalid=True if arp['invalid'] == 'true' else False,
                            arp_is_dynamic=True if arp['dynamic'] == 'true' else False,
                            arp_is_complete=True if arp['complete'] == 'true' else False,
                            arp_is_disabled=True if arp['disabled'] == 'true' else False,
                            arp_is_published=True if arp['published'] == 'true' else False
                        )

                        # Validate if the ARP datatype is correct
                        arp_obj.validate_arp()

                        # Concatenate the ARP data to the list
                        arp_region_list.append(arp_obj)
                    else:
                        # If there is no match, don't add the ARP data to the list
                        # print(arp['address'] + ' not found in the IP segments')
                        pass

                # Concatenate the ARP data to the list
                arp_list.extend(arp_region_list)
            return arp_list
        except Exception as e:
            print(str('Error: get_arp_data: ' + str(e)))

    @staticmethod
    async def add_arp_data(arp_list: list[ARPEntity]) -> None:
        """
        Add available ARP data to the database
        :param arp_list: List of ARP data
        :return: None
        """

        try:
            # Validate all ARP data
            for arp in arp_list:
                arp.validate_arp()

            # Delete all ARP data from the database that are in database but not in the router
            ThreadingManager().run_thread(ARPFunctions.arp_bulk_insert_and_validation, 'w', arp_list)

            # Assign the first tag to the ARP data
            # ThreadingManager().run_thread(ARPTags.assign_first_tag, 'wx')
        except Exception as e:
            print(str('Error: add_arp_data: ' + str(e)))

    @staticmethod
    def ip_scan(router: dict) -> dict:
        """
        Run IP Scan for a specific router
        :param router:
        :return: Dictionary of IP scan data
        """

        try:
            # Create an instance of the RouterAPI class
            router_api_instance = RouterAPI(
                router['ip'],
                router['username'],
                router['password']
            )

            # Set the API connection
            router_api_instance.set_api()

            # Get the IP scan data from the router
            ip_scan_data = RouterAPI.communicate_data(
                router_api_instance.get_api(),
                ['/tool/ip-scan', '=interface=bridgeAPs', '=duration=25s']
            )

            # Return the IP scan data
            return {router['ip']: ip_scan_data}

        except Exception as e:
            raise Exception(f"Error: ip_scan: {e}")

    @staticmethod
    def run_concurrent_ip_scan() -> dict:
        """
        Run IP Scan concurrently for all available routers
        :return: Dictionary of IP scan data from all routers
        """

        try:
            # Import the ThreadPoolExecutor and as_completed modules
            from concurrent.futures import ThreadPoolExecutor, as_completed

            # Get a list of all allowed routers
            routers = ThreadingManager().run_thread(GetAllowedRouters.get, 'r')

            # Dictionary of IP scan data
            results = {}

            # With ThreadPoolExecutor, run the IP scan concurrently for all available routers with a maximum of 40 workers
            with ThreadPoolExecutor(max_workers=40) as executor:
                # Create a dictionary of futures to routers
                future_to_router = {executor.submit(RouterAPI.ip_scan, router): router for router in routers}

                # Iterate through all futures and routers
                for future in as_completed(future_to_router):
                    # router = future_to_router[future]
                    try:
                        # Get the IP scan data from the future
                        data = future.result()

                        # Concatenate the IP scan data to the dictionary
                        results.update(data)
                    except Exception as exc:
                        raise exc

            # Return the IP scan data
            return results
        except Exception as e:
            print(f"Error: run_concurrent_ip_scan: {e}")

    @staticmethod
    def clean_raw_ip_scan_data(raw_dict: dict) -> list[dict]:
        """
        Clean the raw IP scan data dictionary
        :param raw_dict: The raw IP scan data dictionary
        :return: Cleaned IP scan data dictionary
        """

        # Dictionary of cleaned IP scan data
        cleaned_list = []

        # Iterate through all segments and entries in the raw dictionary
        for segment, entries in raw_dict.items():
            # Iterate through all entries in the segment
            for entry in entries:
                # Get the IP and MAC address from the entry
                ip = next((item.split("=")[-1] for item in entry if item.startswith("=address=")), None)
                mac = next((item.split("=")[-1] for item in entry if item.startswith("=mac-address=")), None)

                # Verify if the IP and MAC address are not None
                if ip and mac:
                    cleaned_list.append({ip: mac})
                elif ip:
                    cleaned_list.append({ip: None})

        # Return the cleaned dictionary
        return cleaned_list

    @staticmethod
    def find_duplicates(ip_scan_list: list[dict], ip_main: str, mac_main: str) -> str:
        """
        Find duplicates in the IP scan List
        :param ip_scan_list: Dictionary of IP scan data
        :param ip_main: IP address
        :param mac_main: MAC address
        :return: String of duplicates MAC addresses
        """

        # Dictionary of duplicates
        duplicates = {}

        # Iterate through all items in the IP scan list
        for item in ip_scan_list:
            # Obtain the IP and MAC address from the item
            ip, mac = next(iter(item.items()))

            # Verify if the IP address is not in the duplicates dictionary
            if ip not in duplicates:
                duplicates[ip] = []

            # Verify if the MAC address is not None
            if mac is not None:
                duplicates[ip].append(mac)

        # Return the duplicates MAC addresses
        macs = duplicates.get(ip_main, [])

        # Verify if there are more than one MAC address
        if len(macs) > 1:
            # Return the duplicates MAC addresses
            print(f"IP: {ip_main} has duplicates: {', '.join(macs)}")
            return ', '.join(macs)
        else:
            return ''

    @staticmethod
    async def resolve_ip_duplicity(ip_scan_data: list) -> None:
        try:
            # Import the ARP class and IP Group class
            from models.router_scan.models import ARP
            from models.ip_management.models import IPGroups

            # Get all ARP data from the database
            insert_duplicity_arp, remove_duplicity_arp = [], []
            arp_data = ThreadingManager().run_thread(ARP.get_arps, 'r')

            # Get all IP Groups from the database
            insert_duplicity_ip_group, remove_duplicity_ip_group = [], []
            ip_groups = ThreadingManager().run_thread(IPGroups.get_ip_groups, 'r')

            for arp_data_entry in arp_data:
                # Get the IP and MAC address from the ARP data
                ip_main = arp_data_entry.arp_ip
                mac_main = arp_data_entry.arp_mac

                # Find duplicates in the IP scan data
                duplicates = RouterAPI.find_duplicates(ip_scan_data, ip_main, mac_main)

                # Verify if there are duplicates and ARP data has duplicity as False
                if duplicates != '' and arp_data_entry.ip_duplicity is False:
                    # Set the ARP data duplicity to True and add the duplicates to the ARP data
                    arp_data_entry.ip_duplicity = True
                    arp_data_entry.ip_duplicity_indexes = duplicates

                    # Add the ARP data to the insert list
                    insert_duplicity_arp.append(arp_data_entry)

                elif duplicates == '' and arp_data_entry.ip_duplicity is True:
                    # Append ARP ID to the remove list
                    remove_duplicity_arp.append(arp_data_entry.arp_id)

            # Verify if there are ARP data to insert
            if insert_duplicity_arp:
                # Insert the ARP data with duplicity
                ThreadingManager().run_thread(ARP.bulk_update_duplicity, 'w', insert_duplicity_arp)
            elif remove_duplicity_arp:
                # Remove the ARP data with duplicity
                ThreadingManager().run_thread(ARP.bulk_delete_duplicity, 'w', remove_duplicity_arp)

            for ip_group in ip_groups:
                # Get the IP and MAC address from the ARP data
                ip_main = ip_group[0].ip_group_ip
                mac_main = ip_group[0].ip_group_mac

                # Find duplicates in the IP scan data
                duplicates = RouterAPI.find_duplicates(ip_scan_data, ip_main, mac_main)

                # Verify if there are duplicates and ARP data has duplicity as False
                if duplicates != '' and ip_group[0].ip_duplicity is False:
                    # Set the ARP data duplicity to True and add the duplicates to the ARP data
                    ip_group[0].ip_duplicity = True
                    ip_group[0].ip_duplicity_indexes = duplicates

                    # Add the ARP data to the insert list
                    insert_duplicity_arp.append(ip_group[0])

                elif duplicates == '' and ip_group[0].ip_duplicity is True:
                    # Append ARP ID to the remove list
                    remove_duplicity_arp.append(ip_group[0].ip_group_id)

            # Verify if there are IP Group data to insert
            if insert_duplicity_ip_group:
                # Insert the IP Group data with duplicity
                ThreadingManager().run_thread(IPGroups.bulk_update_duplicity, 'w', insert_duplicity_ip_group)
            elif remove_duplicity_ip_group:
                # Remove the IP Group data with duplicity
                ThreadingManager().run_thread(IPGroups.bulk_delete_duplicity, 'w', remove_duplicity_ip_group)

            print('IP Duplicity resolved')
            print([insert_duplicity_arp, remove_duplicity_arp, insert_duplicity_ip_group, remove_duplicity_ip_group])

        except Exception as e:
            print(str('Error: resolve_ip_duplicity: ' + str(e)))

    @staticmethod
    async def arp_scan():
        """
        Scan ARP data from all available routers
        :return: None
        """
        try:
            # Get the IP segments data and add it to the database
            ip_data = await RouterAPI.get_ip_data()
            await RouterAPI.add_ip_data(ip_data)

            # Get the ARP data and add it to the database
            arp_data = await RouterAPI.get_arp_data()
            await RouterAPI.add_arp_data(arp_data)

            # Get IP Scan information
            raw_ip_scan_data = RouterAPI.run_concurrent_ip_scan()
            cleaned_ip_scan_data = RouterAPI.clean_raw_ip_scan_data(raw_ip_scan_data)

            # Resolve the IP Scan data
            await RouterAPI.resolve_ip_duplicity(cleaned_ip_scan_data)

            # Set the scan status to IDLE
            print('ARP scan finished')
        except Exception as e:
            print(str('Error: arp_scan: ' + str(e)))
