# Description: Functions for the IP Addresses Blueprint

# Importing Necessary Libraries
from app.extensions import db
# Importing Necessary Libraries

# Class for IP Addresses Functions
class IPAddressesFunctions:
    # Constructor
    def __init__(self):  # Constructor
        pass  # Pass the constructor
    # Constructor

    # Function to validate if the IP Segment already exists, based on the IP and Mask and Interface
    @staticmethod
    def validate_ip_segment_exists(ip_segment_ip, ip_segment_mask, ip_segment_interface):
        try:
            # Importing Required Models
            from app.blueprints.ip_addresses.models import IPSegment
            # Importing Required Models

            # Querying the Database
            ip_segment = IPSegment.query.filter(
                IPSegment.ip_segment_ip == ip_segment_ip,  # IP Segment IP
                IPSegment.ip_segment_mask == ip_segment_mask,  # IP Segment Mask
                IPSegment.ip_segment_interface == ip_segment_interface  # IP Segment Interface
            ).first()
            # Querying the Database

            # If the IP Segment exists
            if ip_segment:
                # If the IP Segment ID is different from the IP Segment ID
                if ip_segment_ip != ip_segment.ip_segment_ip and ip_segment_mask != ip_segment.ip_segment_mask and ip_segment_interface != ip_segment.ip_segment_interface:
                    return True  # Return False
                # If the IP Segment ID is different from the IP Segment ID
                return False  # Return True
            else:  # If the IP Segment does not exist
                return True  # Return False
            # If the IP Segment exists
        except Exception as e:  # If an Exception occurs
            print(str(e))  # Print the Exception
    # Function to validate if the IP Segment already exists, based on the IP and Mask and Interface

    # Function to delete IP Segments that are in the database but are not in the router list
    @staticmethod
    def delete_ip_segments(router_segment_list, fk_router_id):
        try:
            # Make a list of Strings IPs with Mask, and Interface Included just for router_segment_list that has the FK_Router_ID
            router_segment_list_p = [str(router_segment.ip_segment_ip) + "/" + str(router_segment.ip_segment_mask) + "@" + str(router_segment.ip_segment_interface) for router_segment in router_segment_list if router_segment.fk_router_id == fk_router_id]
            # Make a list of Strings IPs with Mask, and Interface Included just for router_segment_list that has the FK_Router_ID

            # Importing Required Models
            from app.blueprints.ip_addresses.models import IPSegment
            # Importing Required Models

            # Querying the Database
            ip_segments = IPSegment.query.filter(
                IPSegment.fk_router_id == fk_router_id  # Filter by FK Router ID
            ).all()
            # Querying the Database

            # For each IP Segment in the Database
            for ip_segment in ip_segments:
                # If the IP Segment is not in the router list
                if str(ip_segment.ip_segment_ip) + "/" + str(ip_segment.ip_segment_mask) + "@" + str(ip_segment.ip_segment_interface) not in router_segment_list_p:
                    db.session.delete(ip_segment)  # Delete the IP Segment
            # For each IP Segment in the Database

            db.session.commit()  # Commit the Database Session
        except Exception as e:  # If an Exception occurs
            db.session.rollback()  # Rollback the Database Session
            print(str(e))  # Print the Exception
    # Function to delete IP Segments that are in the database but are not in the router list

    # Function to determine the Tag of an IP Segment
    @staticmethod
    def determine_ip_segment_tag(ip_segment_ip):
        try:
            # Importing Required Entities
            from app.blueprints.ip_addresses.entities import IPSegmentTag

            # Importing Required Models
            from app.blueprints.ip_addresses.models import IPSegment
            # Importing Required Models

            # If the IP Segment exists
            # If IP starts with 10.x.x.x
            if ip_segment_ip.startswith("10."):
                return IPSegmentTag.PRIVATE_IP  # Return Private IP
            else:
                return IPSegmentTag.PUBLIC_IP
            # If the IP Segment exists
        except Exception as e:  # If an Exception occurs
            print(str(e))  # Print the Exception
    # Function to determine the Tag of an IP Segment
# Class for IP Addresses Functions
