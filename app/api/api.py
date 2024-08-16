# Description: File to handle the Router OS API

# Importing Necessary Libraries
import ros_api
# Importing Necessary Libraries

# Importing Necessary Modules
from app.extensions import db
from app.api.modules.GetAllowedRouters import GetAllowedRouters
# Importing Necessary Modules

# Importing Necessary Entities
from app.blueprints.scan.entities import ARPEntity
# Importing Necessary Entities

# Importing Necessary Modules
from app.blueprints.ip_addresses.models import IPSegment
# Importing Necessary Modules

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
    def get_ip_data(router_id) -> list:
        ip_list = []  # IP list
        routers = GetAllowedRouters(db).get()
        for router in routers:
            print(
                router.router_ip,
                router.router_username,
                router.router_password
            )
        """
        for router in routers:  # Loop through the routers
            router_api = RouterAPI(  # Create an instance of the RouterAPI class
                router.router_ip,  # Router IP
                router.router_username,  # Router username
                router.router_password  # Router password
            )
            router_api.set_api()  # Set the API object
            ip_data = RouterAPI.retrieve_data(router_api.get_api(), '/ip/address/print')  # Retrieve IP data
            for ip in ip_data:
                ip_list.append(  # Append the IP data to the IP list
                    IPSegmentEntity(  # Create an instance of the IPSegmentEntity class
                        ip_segment_id=ip['.id'],  # IP Segment ID
                        fk_router_id=router_id,  # FK Router ID
                        ip_segment_ip=ip['address'],  # IP Segment IP
                        ip_segment_mask=ip['netmask'],  # IP Segment Mask
                        ip_segment_network=ip['network'],  # IP Segment Network
                        ip_segment_interface=ip['interface'],  # IP Segment Interface
                        ip_segment_actual_iface=ip['actual-interface'],  # IP Segment Actual Interface
                        ip_segment_tag=ip['comment'],  # IP Segment Tag
                        ip_segment_comment=ip['comment'],  # IP Segment Comment
                        ip_segment_is_invalid=ip['invalid'],  # IP Segment Is Invalid
                        ip_segment_is_dynamic=ip['dynamic'],  # IP Segment Is Dynamic
                        ip_segment_is_disabled=ip['disabled']  # IP Segment Is Disabled
                    )
                )
                IPSegmentEntity.validate_ip_segment()  # Validate the IP Segment Entity
        return ip_list  # Return the IP list
        """
    # Method to get IP address data from the Router OS API and save it to the database

    # Method to add IP address data to the database
    @staticmethod
    def add_ip_data(ip_list) -> None:
        for ip in ip_list:
            ip_segment = IPSegment(  # Create an instance of the IPSegment class
                ip_segment_id=ip.ip_segment_id,  # IP Segment ID
                fk_router_id=ip.fk_router_id,  # FK Router ID
                ip_segment_ip=ip.ip_segment_ip,  # IP Segment IP
                ip_segment_mask=ip.ip_segment_mask,  # IP Segment Mask
                ip_segment_network=ip.ip_segment_network,  # IP Segment Network
                ip_segment_interface=ip.ip_segment_interface,  # IP Segment Interface
                ip_segment_actual_iface=ip.ip_segment_actual_iface,  # IP Segment Actual Interface
                ip_segment_tag=ip.ip_segment_tag,  # IP Segment Tag
                ip_segment_comment=ip.ip_segment_comment,  # IP Segment Comment
                ip_segment_is_invalid=ip.ip_segment_is_invalid,  # IP Segment Is Invalid
                ip_segment_is_dynamic=ip.ip_segment_is_dynamic,  # IP Segment Is Dynamic
                ip_segment_is_disabled=ip.ip_segment_is_disabled  # IP Segment Is Disabled
            )
            try:
                IPSegment.add_ip_segment(ip_segment)
            except Exception as e:
                pass
    # Method to add IP address data to the database

    # Method to get the data from ARP data, and return it as list of ARP objects
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
            router_api.set_api()  # Set the API object
            arp_data = RouterAPI.retrieve_data(router_api.get_api(), '/ip/arp/print')  # Retrieve ARP data
            for arp in arp_data:  # Loop through the ARP data
                arp_list.append(  # Append the ARP data to the ARP list
                    ARPEntity(  # Create an instance of the ARPEntity class
                        arp_id=arp['.id'],  # ARP ID
                        fk_ip_address_id=router.router_id,  # FK IP Address ID
                        arp_ip=arp['address'],  # ARP IP
                        arp_mac=arp['mac-address'],  # ARP MAC
                        arp_tag=arp['tag'],  # ARP Tag
                        arp_interface=arp['interface'],  # ARP Interface
                        arp_is_dhcp=arp['dynamic'],  # ARP DHCP
                        arp_is_invalid=arp['invalid'],  # ARP Invalid
                        arp_is_dynamic=arp['dynamic'],  # ARP Dynamic
                        arp_is_complete=arp['complete'],  # ARP Complete
                        arp_is_disabled=arp['disabled'],  # ARP Disabled
                        arp_is_published=arp['published']  # ARP Published
                    )
                )
        return arp_list  # Return the ARP list
    # Method to get the data from ARP data, and return it as list of ARP objects
    # Static Methods
# Class to handle the RouterOS API

# Main function
def main():
    pass
# Main function

# Running the main function
if __name__ == '__main__':
    main()
# Running the main function
