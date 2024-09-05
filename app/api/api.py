# Description: File to handle the Router OS API

# Importing Necessary Libraries
import json
import ros_api
from app.blueprints.routers.models import Router
from app.blueprints.router_scan.functions import ARPFunctions
# Importing Necessary Libraries

# Importing Necessary Modules
from app.extensions import db
from app.api.modules.FindIPSegment import FindIPSegment
from app.api.modules.GetAllowedRouters import GetAllowedRouters
# Importing Necessary Modules

# Importing Necessary Entities
from app.blueprints.router_scan.entities import ARPEntity, ARPTag
from app.blueprints.ip_management.entities import IPSegmentEntity
# Importing Necessary Entities

# Importing Necessary Modules
from app.blueprints.router_scan.models import ARP, ARPTags
from app.blueprints.ip_management.models import IPSegment
# Importing Necessary Modules

# Importing Necessary Functions
from app.blueprints.ip_management.functions import IPAddressesFunctions
# Importing Necessary Functions

# Class to handle the Router OS API
class RouterAPI:
    router = None  # Router OS API object
    credentials = None  # Router OS credentials

    # Constructor
    def __init__(
        self,  # Constructor
        host,  # Router OS host
        user,  # Router OS user
        password  # Router OS password
    ):
        self.router = None
        self.credentials = {
            'host': host,
            'user': user,
            'password': password
        }
    # Constructor

    # Getters and Setters
    # Method to get the credentials
    def get_credentials(self):
        return self.credentials  # Return the credentials
    # Method to get the credentials

    # Method to set the credentials
    def set_credentials(
        self,  # Method to set the credentials
        host=None,  # Router OS host
        user=None,  # Router OS user
        password=None  # Router OS password
    ):
        self.credentials = {  # Set the credentials
            'host': host,
            'user': user,
            'password': password
        }
    # Method to set the credentials

    # Method to get the API object
    def get_api(self):
        return self.router  # Return the API object
    # Method to get the API object

    # Method to set the API object
    def set_api(self):
        self.router = ros_api.Api(  # Set the API object
            self.credentials['host'],  # Router OS host
            self.credentials['user'],  # Router OS user
            self.credentials['password'],  # Router OS password
            port=7372,  # Router OS API port
            use_ssl=True  # Use SSL
        )
    # Method to set the API object
    # Getters and Setters

    # Static Methods
    # Method to retrieve data via command talk from the Router OS API
    @staticmethod
    def retrieve_data(router, command) -> dict:
        return router.talk(command)  # Retrieve data via command talk from the Router OS API
    # Method to retrieve data via command talk from the Router OS API

    # Method to get IP address data from the Router OS API and save it to the database
    # Also check that the information don't already exist in the database
    @staticmethod
    def get_ip_data() -> list:
        ip_list = []  # IP list
        routers = GetAllowedRouters(db).get()  # Get all allowed routers
        for router in routers:  # Loop through the routers
            router_api = RouterAPI(  # Create an instance of the RouterAPI class
                router.router_ip,  # Router IP
                router.router_username,  # Router username
                router.router_password  # Router password
            )
            router_api.set_api()  # Set the API object
            router_id = router.router_id  # Router ID
            ip_data = RouterAPI.retrieve_data(router_api.get_api(), '/ip/address/print')  # Retrieve IP data
            for ip in ip_data:
                comment = "None"
                if 'comment' in ip:
                    comment = ip['comment']
                ip_tmp = ip['address'].split('/')  # Split the IP and Mask
                ip_obj = IPSegmentEntity(  # Create an instance of the IPSegmentEntity class
                    ip_segment_id=int(),  # IP Segment ID
                    fk_router_id=router_id,  # FK Router ID
                    ip_segment_ip=ip_tmp[0],  # IP Segment IP
                    ip_segment_mask=ip_tmp[1],  # IP Segment Mask
                    ip_segment_network=ip['network'],  # IP Segment Network
                    ip_segment_interface=ip['interface'],  # IP Segment Interface
                    ip_segment_actual_iface=ip['actual-interface'],  # IP Segment Actual Interface
                    ip_segment_tag=IPAddressesFunctions.determine_ip_segment_tag(
                        ip_tmp[0],  # IP Segment IP
                    ),  # IP Segment Tag
                    ip_segment_comment=comment,  # IP Segment Comment
                    ip_segment_is_invalid=True if ip['invalid'] == 'true' else False,  # IP Segment Is Invalid
                    ip_segment_is_dynamic=True if ip['dynamic'] == 'true' else False,  # IP Segment Is Dynamic
                    ip_segment_is_disabled=True if ip['disabled'] == 'true' else False  # IP Segment Is Disabled
                    )
                ip_obj.validate_ip_segment()  # Validate the IP Segment
                ip_list.append(ip_obj)  # Append the IP object to the IP list
            # Delete IP Segments that are in the database but are not in the router list
            IPAddressesFunctions.delete_ip_segments(ip_list, router.router_id)  # Delete IP Segments
            # Delete IP Segments that are in the database but are not in the router list
        return ip_list  # Return the IP list
    # Method to get IP address data from the Router OS API and save it to the database

    # Method to add IP address data to the database
    @staticmethod
    def add_ip_data(ip_list):
        try:
            for ip in ip_list:  # For each IP
                try:  # Try to add the IP Segment
                    ip.validate_ip_segment()  # Validate the IP Segment
                    IPSegment.add_ip_segment(ip)  # Add the IP Segment
                except Exception as e:  # If an Exception occurs
                    print(str(e))  # Print the Exception
        except Exception as e:  # If an Exception occurs
            print(str(e))  # Print the Exception
    # Method to add IP address data to the database

    # Method to get ARP data from the Router OS API and save it to the database
    @staticmethod
    def get_arp_data() -> list:
        arp_list = []  # ARP list
        routers = GetAllowedRouters(db).get()  # Get all allowed routers
        for router in routers:  # Loop through the routers
            router_api = RouterAPI(  # Create an instance of the RouterAPI class
                router.router_ip,  # Router IP
                router.router_username,  # Router username
                router.router_password  # Router password
            )
            arp_region_list = []  # ARP region list
            router_api.set_api()  # Set the API object

            router_id = router.router_id  # Router ID
            ip_segments_by_router = IPSegment.get_ip_segments_by_router_id(router_id)  # Get IP segments by router ID
            arp_data = RouterAPI.retrieve_data(router_api.get_api(), '/ip/arp/print')  # Retrieve ARP data

            # Getting Queue List from Router
            queue_data = RouterAPI.retrieve_data(router_api.get_api(), '/queue/simple/print')
            # Getting Queue List from Router
            # Create a dictionary of key:value pairs with the ARP IP and Name
            queue_dict = {}
            for queue in queue_data:
                name = queue['name']
                ip = queue['target'].split('/')[0]
                queue_dict[ip] = name
            # Create a dictionary of key:value pairs with the ARP IP and Name

            for arp in arp_data:
                ip_segment = FindIPSegment.find(ip_segments_by_router, arp['address'])  # Find the IP segment
                if ip_segment[0] is True:  # If the IP segment is found
                    arp_obj = ARPEntity(  # Create an instance of the ARPEntity class
                        arp_id=int(),  # ARP ID
                        fk_ip_address_id=int(ip_segment[1]),  # FK IP Address ID
                        arp_ip=arp['address'],  # ARP IP
                        arp_mac="" if 'mac-address' not in arp else arp['mac-address'],  # ARP MAC
                        arp_alias=ARPFunctions.assign_alias(str(arp['address']), queue_dict),  # ARP Alias
                        arp_interface=arp['interface'],  # ARP Interface
                        arp_is_dhcp=True if arp['dynamic'] == 'true' else False,  # ARP DHCP
                        arp_is_invalid=True if arp['invalid'] == 'true' else False,  # ARP Invalid
                        arp_is_dynamic=True if arp['dynamic'] == 'true' else False,  # ARP Dynamic
                        arp_is_complete=True if arp['complete'] == 'true' else False,  # ARP Complete
                        arp_is_disabled=True if arp['disabled'] == 'true' else False,  # ARP Disabled
                        arp_is_published=True if arp['published'] == 'true' else False  # ARP Published
                    )
                    arp_obj.validate_arp()  # Validate the ARP
                    arp_region_list.append(arp_obj)  # Append the ARP object to the ARP list
                else:
                    pass
            # Delete ARPs that are in the database but are not in the router list
            ARPFunctions.delete_arps(arp_region_list, router.router_id, ARPTags)
            # Delete ARPs that are in the database but are not in the router list
            arp_list.extend(arp_region_list)  # Extend the ARP list
        return arp_list  # Return the ARP list
    # Method to get ARP data from the Router OS API and save it to the database

    # Method to add ARP data to the database
    @staticmethod
    def add_arp_data(arp_list):
        try:
            for arp in arp_list:  # For each ARP
                try:  # Try to add the ARP
                    ARP.add_arp(arp)  # Add the ARP
                except Exception as e:  # If an Exception occurs
                    print(str(e))  # Print the Exception
            ARPTags.assign_first_tag()  # Assign the first tag
        except Exception as e:  # If an Exception occurs
            print(str(e))  # Print the Exception
    # Method to add ARP data to the database

    # Method to router_scan arp data from the Router OS API
    @staticmethod
    def arp_scan():
        RouterAPI.add_ip_data(RouterAPI.get_ip_data())  # Add IP data to the database
        RouterAPI.add_arp_data(RouterAPI.get_arp_data())  # Add ARP data to the database
    # Method to router_scan arp data from the Router OS API
    # Static Methods
# Class to handle the RouterOS API

# Main function - ONLY FOR TESTING
def main():
    pass  # Do nothing  # Password: N0c#2024.@!!
# Main function - ONLY FOR TESTING

# Running the main function
if __name__ == '__main__':
    main()
# Running the main function
