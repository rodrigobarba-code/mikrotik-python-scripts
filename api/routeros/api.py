"""
# Version: 1.0
This file contains the RouterAPI class that is used to communicate with the RouterOS API.
Also, the RouterAPI class is the kernel of the ARP scan process, as it contains all the methods to communicate with the RouterOS API.

The RouterAPI class contains the following methods:
    - __init__:
        Initializes the RouterAPI class
    - get_scan_status:
        Gets the scan status
    - set_scan_status:
        Sets the scan status
    - get_credentials:
        Gets the credentials
    - set_credentials:
        Sets the credentials
    - get_api:
        Gets the API
    - set_api:
        Sets the API
    - retrieve_data:
        Retrieves data from the router
    - communicate_data:
        Communicates data with the router
    - verify_router_connection:
        Verifies the router connection
    - get_ip_data:
        Gets IP data from all available routers
    - add_ip_data:
        Adds IP data to the database
    - get_arp_data:
        Gets ARP data from all available routers
    - add_arp_data:
        Adds ARP data to the database
    - ip_scan:
        Runs IP scan for a specific router
    - run_concurrent_ip_scan:
        Runs IP scan concurrently for all available routers
    - clean_raw_ip_scan_data:
        Cleans the raw IP scan data dictionary
    - find_duplicates:
        Finds duplicates in the IP scan list
    - resolve_ip_duplicity:
        Resolves IP duplicity
    - arp_scan:
        Scans ARP data from all available routers
"""

# Import the necessary libraries
import asyncio
import ros_api

# Import the mac_vendor_lookup library
from mac_vendor_lookup import MacLookup, BaseMacLookup

# Import the necessary classes for entities
from entities.ip_groups import IPGroupsEntity
from entities.ip_segment import IPSegmentEntity

# Import the necessary classes for models
from models.ip_management.models import IPSegment
from models.router_scan.functions import ARPFunctions
from models.ip_management.functions import IPAddressesFunctions

# Import the necessary classes for threading and socketio
from utils.threading_manager import ThreadingManager
from websockets.socketio_manager import SocketIOManager

# Import the necessary modules for the API
from api.routeros.modules.FindIPSegment import FindIPSegment
from api.routeros.modules.GetAllowedRouters import GetAllowedRouters

class RouterAPI:
    router = None  # Router instance
    credentials = None  # Credentials dictionary

    # Constructor for the RouterAPI class
    def __init__(
            self,
            host,
            user,
            password
    ):
        """
        Initialize the RouterAPI class
        :param host: Hostname or IP address
        :param user: Username of Router Mikrotik
        :param password: Password of Router Mikrotik
        """
        self.router = None
        self.credentials = {
            'host': host,
            'user': user,
            'password': password
        }

    # Get credentials
    def get_credentials(self):
        """
        Get the credentials for the RouterAPI
        :return: Dictionary of credentials
        """
        return self.credentials

    # Set credentials
    def set_credentials(
            self,
            host=None,
            user=None,
            password=None
    ):
        """
        Set the credentials for the RouterAPI
        :param host: Hostname or IP address
        :param user: Username of Router Mikrotik
        :param password: Password of Router Mikrotik
        :return: None
        """
        self.credentials = {
            'host': host,
            'user': user,
            'password': password
        }

    # Get API Router instance
    def get_api(self):
        """
        Get the API connection
        :return: API Router instance
        """
        return self.router

    # Set API Router instance
    def set_api(self):
        """
        Set the API connection
        :return: None
        """
        self.router = ros_api.Api(
            self.credentials['host'],
            self.credentials['user'],
            self.credentials['password'],
            port=7372,
            use_ssl=True
        )

    # Retrieve data from the router, using the talk method, which is a synchronous method
    @staticmethod
    def retrieve_data(router, command) -> dict:
        """
        Retrieve data from the router
        :param router: RouterAPI instance
        :param command: Command to retrieve data
        :return: Dictionary of data
        """
        try:
            return router.talk(command)
        except Exception as e:
            print(str('Error: retrieve_data: ' + str(e)))

    # Communicate data with the router, using the communicate method, which is an asynchronous method and can send multiple commands and parameters
    @staticmethod
    def communicate_data(router, command: list[str]) -> dict:
        """
        Communicate data with the router
        :param router: RouterAPI instance
        :param command: Command to communicate
        :return:
        """
        try:
            return router.communicate(command)
        except Exception as e:
            print(str('Error: communicate_data: ' + str(e)))

    # Verify the router connection
    @staticmethod
    def verify_router_connection(router) -> bool:
        """
        Verify the router connection
        :param router:  RouterAPI instance
        :return: True if the connection is successful, False otherwise
        """
        try:
            router.talk('/system/resource/print')
            return True
        except (Exception, asyncio.TimeoutError) as e:
            raise e

    # Get IP data from all available routers
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
                ThreadingManager().run_thread(IPSegment.verify_autoincrement_id, 'r')
            return ip_list
        except Exception as e:
            print(str('Error: get_ip_data: ' + str(e)))

    # Add IP data to the database
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

    # Get ARP data from all available routers
    @staticmethod
    async def get_arp_data() -> list:
        """
        Get ARP data from all available routers
        :return: List of ARP data
        """

        try:
            # List of ARP data
            ip_group_list = []

            # Set the cache path for the MAC lookup
            BaseMacLookup.cache_path = "./mac.txt"
            mac = MacLookup()

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
                ip_group_region_list = []

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
                        ip_group_obj = IPGroupsEntity(
                            ip_group_id=int(),
                            fk_ip_segment_id=int(ip_segment[1]),
                            ip_group_name=ARPFunctions.determine_arp_name(arp['dynamic'], arp['complete'], '' if 'mac-address' not in arp else arp['mac-address'],),
                            ip_group_type='public' if ARPFunctions.determine_arp_tag(arp['address']) == 'Public IP' else 'private',
                            ip_group_alias=ARPFunctions.assign_alias(arp['address'], queue_dict),
                            ip_group_description="No description",
                            ip_group_ip=arp['address'],
                            ip_group_mask=ThreadingManager().run_thread(ARPFunctions.determine_arp_mask, 'rx', ip_segment[1]),
                            ip_group_mac="" if 'mac-address' not in arp else arp['mac-address'],
                            ip_group_mac_vendor='',
                            ip_group_interface=arp['interface'],
                            ip_group_comment="No comment",
                            ip_is_dhcp=True if arp['dynamic'] == 'true' else False,
                            ip_is_dynamic=True if arp['dynamic'] == 'true' else False,
                            ip_is_complete=True if arp['complete'] == 'true' else False,
                            ip_is_disabled=True if arp['disabled'] == 'true' else False,
                            ip_is_published=True if arp['published'] == 'true' else False,
                            ip_duplicity=False,
                            ip_duplicity_indexes=""
                        )

                        # Validate if the ARP datatype is correct
                        ip_group_obj.validate_ip_group()

                        # Concatenate the ARP data to the list
                        ip_group_region_list.append(ip_group_obj)
                    else:
                        # If there is no match, don't add the ARP data to the list
                        # print(arp['address'] + ' not found in the IP segments')
                        pass

                # Concatenate the ARP data to the list
                ip_group_list.extend(ip_group_region_list)
            return ip_group_list
        except Exception as e:
            print(str('Error: get_arp_data: ' + str(e)))

    # Add ARP data to the database
    @staticmethod
    async def add_arp_data(ip_group_list: list[IPGroupsEntity]) -> None:
        """
        Add available ARP data to the database
        :param ip_group_list: List of ARP data
        :return: None
        """

        try:
            # Delete all ARP data from the database that are in database but not in the router
            ThreadingManager().run_thread(ARPFunctions.place_ip_group_on_table, 'w', ip_group_list)
        except Exception as e:
            print(str('Error: add_arp_data: ' + str(e)))

    # Run IP scan for a specific router
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
                ['/tool/ip-scan', '=interface=bridgeAPs', '=duration=90s']
            )

            # Return the IP scan data
            return {router['ip']: ip_scan_data}

        except Exception as e:
            raise Exception(f"Error: ip_scan: {e}")

    # Run IP scan concurrently for all available routers
    @staticmethod
    def run_concurrent_ip_scan() -> dict:
        """
        Run IP Scan concurrently for all available routers
        :return: Dictionary of IP scan data from all routers
        """

        try:
            # Import the ThreadPoolExecutor and as_completed modules
            import re
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
                    router_ip = future_to_router[future]['ip']
                    try:
                        # Get the IP scan data from the future
                        raw_data = future.result()

                        # Reverse the list elements and get the first element
                        reverse = list(raw_data.values())[0]
                        reverse.reverse()

                        # Get the last section of IP Scan using REGEX to find =.section=*
                        last_section_string = [item for item in reverse[1] if item.startswith('=.section=')][0]

                        # Remove all elements that are not the last section of IP Scan
                        reverse.pop(0)

                        # Iterate through all elements in the reversed list
                        reverse_mod = [sublist for sublist in reverse if last_section_string in sublist]
                        reverse_mod.reverse()

                        # Concatenate the IP scan data to the results dictionary
                        dict_mod = {router_ip: reverse_mod}
                        results.update(dict_mod)
                    except Exception as exc:
                        raise exc

            # Return the IP scan data
            return results
        except Exception as e:
            print(f"Error: run_concurrent_ip_scan: {e}")

    # Clean the raw IP scan data dictionary
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

    # Find duplicates in the IP scan list
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
            if mac is not None and mac != mac_main:
                duplicates[ip].append(mac)

        # Return the duplicates MAC addresses
        macs = duplicates[ip_main] if ip_main in duplicates else []

        # Verify if there are more than one MAC address
        if len(macs) > 0:
            # Return the duplicates MAC addresses
            return ', '.join(macs)
        else:
            return ''

    # Resolve IP duplicity
    @staticmethod
    async def resolve_ip_duplicity(ip_scan_data: list) -> None:
        try:
            # Import the ARP class and IP Group class
            from models.router_scan.models import ARP
            from models.ip_management.models import IPGroups

            # Get all IP Groups from the database
            to_update = []
            ip_groups = ThreadingManager().run_thread(IPGroups.get_ip_groups, 'r')

            for ip_group in ip_groups:
                # Get the IP and MAC address from the ARP data
                ip_main = ip_group[0].ip_group_ip
                mac_main = ip_group[0].ip_group_mac

                # Find duplicates in the IP scan data
                duplicates = RouterAPI.find_duplicates(ip_scan_data, ip_main, mac_main)

                # Verify if there are duplicates and ARP data has duplicity as False
                if duplicates != '' and ip_group[0].ip_duplicity is False:
                    # Create IP Group object with duplicity
                    ip_group[0].ip_duplicity = True
                    ip_group[0].ip_duplicity_indexes = duplicates

                    to_update.append(ip_group[0])

            # Clean the ARP data from the database
            ThreadingManager().run_thread(ARP.delete_all_arps, 'wx')

            # Restore autoincrement ID
            ThreadingManager().run_thread(ARP.verify_autoincrement_id, 'wx')

            # Verify if there are IP Group data to insert
            if to_update:
                # Insert the ARP data to the database
                ThreadingManager().run_thread(ARP.bulk_insert_from_ip_groups, 'w', to_update)

                # Change duplicity status to True
                ip_group_ids = [int(ip_group.ip_group_id) for ip_group in to_update]
                ThreadingManager().run_thread(IPGroups.change_duplicity_to_true, 'rx', ip_group_ids)

                # Delete IP Group data with duplicity as True
                ThreadingManager().run_thread(IPGroups.delete_duplicity_on_table, 'wx')

            print('IP duplicity resolved, we found ' + str(len(to_update)) + ' duplicities')
        except Exception as e:
            print(str('Error: resolve_ip_duplicity: ' + str(e)))

    # Scan ARP data from all available routers
    @staticmethod
    async def arp_scan():
        """
        Scan ARP data from all available routers
        :return: None
        """
        try:
            # Create variables for the message and percentage
            message = ''
            percent = 0

            # Get socket instance
            socketio = SocketIOManager.get_instance()

            # Set the scan status to IN PROGRESS
            SocketIOManager.set_scan_status(1)

            """Get IP Segments"""

            # Get the IP segments data and add it to the database
            ip_data = await RouterAPI.get_ip_data()

            # Set the message and percentage for the scan status
            percent = 25
            message = 'Obtaining IP segments data from the available routers'

            # Set the message and percentage for the scan status
            SocketIOManager.set_message(message)
            SocketIOManager.set_percent(percent)

            # Emit the scan status to the frontend
            socketio.emit(
                'scan_status',
                {
                    'scan_status': message,
                    'percentage': percent
                }
            )

            """Add IP Segments"""

            # Add the IP segments data to the database
            await RouterAPI.add_ip_data(ip_data)

            # Set the message and percentage for the scan status
            percent = 50
            message = 'Adding IP segments data to the database'

            # Set the message and percentage for the scan status
            SocketIOManager.set_message(message)
            SocketIOManager.set_percent(percent)

            socketio.emit(
                'scan_status',
                {
                    'scan_status': message,
                    'percentage': percent
                }
            )

            """Get ARP Data"""

            # Get the ARP data and add it to the database
            arp_data = await RouterAPI.get_arp_data()

            # Set the message and percentage for the scan status
            percent = 75
            message = 'Getting ARP data from the available routers'

            # Set the message and percentage for the scan status
            SocketIOManager.set_message(message)
            SocketIOManager.set_percent(percent)

            # Emit the scan status to the frontend
            socketio.emit(
                'scan_status',
                {
                    'scan_status': message,
                    'percentage': percent
                }
            )

            """Add ARP Data"""

            # Add the ARP data to the database
            await RouterAPI.add_arp_data(arp_data)

            # Set the message and percentage for the scan status
            percent = 85
            message = 'Adding ARP data to the database'

            # Set the message and percentage for the scan status
            SocketIOManager.set_message(message)
            SocketIOManager.set_percent(percent)

            # Set the message and percentage for the scan status
            socketio.emit(
                'scan_status',
                {
                    'scan_status': message,
                    'percentage': percent
                }
            )

            """Get IP Scan Data"""

            # Get IP Scan information
            raw_ip_scan_data = RouterAPI.run_concurrent_ip_scan()
            cleaned_ip_scan_data = RouterAPI.clean_raw_ip_scan_data(raw_ip_scan_data)

            # Set the message and percentage for the scan status
            percent = 95
            message = 'Running IP Scan for all available routers'

            # Set the message and percentage for the scan status
            SocketIOManager.set_message(message)
            SocketIOManager.set_percent(percent)

            # Emit the scan status to the frontend
            socketio.emit(
                'scan_status',
                {
                    'scan_status': message,
                    'percentage': percent
                }
            )

            """Resolve IP Duplicity"""

            # Resolve the IP Scan data
            await RouterAPI.resolve_ip_duplicity(cleaned_ip_scan_data)

            # Set the message and percentage for the scan status
            percent = 99
            message = 'Resolving IP duplicity using IP Scan data'

            # Set the message and percentage for the scan status
            socketio.emit(
                'scan_status',
                {
                    'scan_status': message,
                    'percentage': percent
                }
            )

            """Finish ARP Scan"""

            # Emit the scan status to the frontend
            socketio.emit('scan_complete', {'scan_status': 'ARP scan finished'})

            # Set the scan status to IDLE
            SocketIOManager.set_scan_status(0)

            # Print the ARP scan finished message
            print('ARP scan finished')
        except Exception as e:
            print(str('Error: arp_scan: ' + str(e)))
