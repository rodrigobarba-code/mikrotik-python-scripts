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
    def find(ip_segments, arp_ip) -> int:
        try:  # Try to find the IP Segment
            with current_app.app_context():  # Create a context
                arp_ip_obj = ipaddress.ip_address(arp_ip)  # ARP IP Object
                for segment in ip_segments:
                    ip = segment.ip_segment_ip + "/" + segment.ip_segment_mask  # IP Segment
                    network = ipaddress.ip_network(ip, strict=False)  # IP Network
                    if arp_ip_obj in network:  # If the ARP IP is in the network
                        return int(segment.ip_segment_id)  # Return the IP Segment ID
                    else:
                        return 1  # Return 1
        except Exception as e:  # Catch any exceptions
            # Return an error message
            print(str("An error occurred while finding the IP Segment: " + str(e)))
    # Method to find IP Segment
# Class to find IP Segment
