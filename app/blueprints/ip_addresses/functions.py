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
            # Importing Required Models
            from app.blueprints.ip_addresses.models import IPSegment
            # Importing Required Models

            # Querying the Database
            database_segment_list = []  # Database Segment List
            ip_segments = IPSegment.query.filter(  # Query the IP Segments
                IPSegment.fk_router_id == fk_router_id  # FK Router ID
            ).all()  # Get all results
            for ip_segment in ip_segments:  # For each IP Segment
                # Create a tuple with the IP and Mask and Interface in a String format
                database_segment_list.append([ip_segment.ip_segment_ip, ip_segment.ip_segment_mask, ip_segment.ip_segment_interface, ip_segment.ip_segment_id])
            # Querying the Database

            # For each Database Segment
            # For each Database Segment
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
# Class for IP Addresses Functions
