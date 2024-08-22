# Description: File to handle the Router OS API

# Importing Necessary Libraries
import ros_api
# Importing Necessary Libraries

# Importing Necessary Modules
from app.extensions import db
from app.api.modules.GetAllowedRouters import GetAllowedRouters
# Importing Necessary Modules

# Importing Necessary Entities
from app.blueprints.ip_addresses.entities import IPSegmentEntity
# Importing Necessary Entities

# Importing Necessary Modules
from app.blueprints.ip_addresses.models import IPSegment
# Importing Necessary Modules

# Importing Necessary Functions
from app.blueprints.ip_addresses.functions import IPAddressesFunctions
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
                try:  # Try to get the comment
                    comment = ip['comment']  # Get the comment
                except:  # If an exception occurs
                    pass  # Do nothing
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

    # Method to scan arp data from the Router OS API
    @staticmethod
    def scan_arp() -> list:
        RouterAPI.add_ip_data(RouterAPI.get_ip_data())  # Add IP data to the database
        return True  # Return True
    # Method to scan arp data from the Router OS API
    # Static Methods
# Class to handle the RouterOS API

# Main function - ONLY FOR TESTING
def main():
    pass  # Do nothing
# Main function - ONLY FOR TESTING

# Running the main function
if __name__ == '__main__':
    main()
# Running the main function
