# Description: Module to find the IP Segment of ARP IP

# Importing necessary modules
import ipaddress
from flask import current_app
# Importing necessary modules

# Class to find IP Segment
class FindIPSegment:
    # Constructor
    def __init__(
        self,  # Constructor
        db=None  # Database object
    ):
        self.db = db  # Setting the database object
    # Constructor

    # Method to find IP Segment
    @staticmethod
    def find(ip_segments, arp_ip) -> list:
        try:  # Try to find the IP Segment
            with current_app.app_context():  # Create a context
                ip = ipaddress.ip_address(arp_ip)  # IP Object
                # Create a set of all the IP addresses in the network
                ip_segments_set = [[segment.ip_segment_id, segment.ip_segment_ip, segment.ip_segment_ip+ "/" + segment.ip_segment_mask] for segment in ip_segments]
                # Create a set of all the IP addresses in the network
                for ip_network in ip_segments_set:  # For each segment
                    network = ipaddress.ip_network(ip_network[2], strict=False)  # IP Network
                    if ip in network:  # If the IP is in the network
                        return [True, int(ip_network[0])]  # Return the IP Segment ID
                else:  # If the IP Segment is not found
                    return [False, None]  # Return False
        except Exception as e:  # Catch any exceptions
            # Return an error message
            print(str("An error occurred while finding the IP Segment: " + str(e)))
    # Method to find IP Segment
# Class to find IP Segment
