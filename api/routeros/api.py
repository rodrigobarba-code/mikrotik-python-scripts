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
    async def get_ip_duplicates() -> dict:
        """
        Get IP duplicates from the database
        :return: Dictionary with the IP duplicates
        """

        # Importing here to avoid circular imports
        from models.ip_management.functions import IPAddressesFunctions

        try:
            # Get the IP duplicates
            result = ThreadingManager().run_thread(IPAddressesFunctions.find_ip_duplicates, 'r')

            # Return the IP duplicates
            return result
        except Exception as e:
            print(str('Error: get_ip_duplicates: ' + str(e)))

    @staticmethod
    async def validate_ip_duplicates():
        """
        Validate IP duplicates in the database
        :return: None
        """

        try:
            # Get all IP segments
            ip_segments = ThreadingManager().run_thread(IPSegment.get_all_ip_segments, 'r')

            # Validate all IP segments
            for ip in ip_segments:
                ip.validate_ip_segment()

            # Delete all IP segments from the database that are in database but not in the router
            ThreadingManager().run_thread(IPAddressesFunctions.delete_ip_segments, 'w', ip_segments)
        except Exception as e:
            print(str('Error: validate_ip_duplicates: ' + str(e)))

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

            # Resolve IP Duplicates
            ip_duplicates = await RouterAPI.get_ip_duplicates()
            print('IP Duplicates: ' + str(ip_duplicates))

            print('ARP scan finished')
        except Exception as e:
            print(str('Error: arp_scan: ' + str(e)))
