# Description: Functions for the IP Addresses Blueprint

# Importing Necessary Libraries
import json
from app.extensions import db
from collections import Counter
# Importing Necessary Libraries

# Importing Necessary Entities
from app.blueprints.scan.entities import ARPTag
# Importing Necessary Entities

# Importing Necessary Models
from app.blueprints.ip_addresses.models import IPSegment
# Importing Necessary Models

# Class for ARP Functions
class ARPFunctions:
    # Constructor
    def __init__(self):  # Constructor
        pass  # Pass the constructor
    # Constructor

    # Function to validate if the ARP already exists, based on the IP and MAC
    @staticmethod
    def validate_arp_exists(arp_ip, arp_mac):
        try:
            # Importing Required Models
            from app.blueprints.scan.models import ARP
            # Importing Required Models

            # Querying the Database
            arp = ARP.query.filter(
                ARP.arp_ip == arp_ip,  # ARP IP
                ARP.arp_mac == arp_mac  # ARP MAC
            ).first()
            # Querying the Database

            # If the ARP exists
            if arp:
                # If the ARP ID is different from the ARP ID
                if arp_ip != arp.arp_ip and arp_mac != arp.arp_mac:
                    return True  # Return False
                # If the ARP ID is different from the ARP ID
                return False  # Return True
            else:  # If the ARP does not exist
                return True  # Return False
            # If the ARP exists
        except Exception as e:  # If an Exception occurs
            print(str(e))  # Print the Exception
    # Function to validate if the ARP already exists, based on the IP and MAC

    # Function to delete ARPs that are in the database but are not in the router list
    @staticmethod
    def delete_arps(router_arp_list, fk_router_id):
        try:
            # Make a list of Strings IPs with Mask, and Interface Included just for router_arp_list that has the FK_Router_ID
            router_arp_list_p = [str(router_arp.arp_ip) + "@" + str(router_arp.arp_mac) for router_arp in router_arp_list]
            # Make a list of Strings IPs with Mask, and Interface Included just for router_arp_list that has the FK_Router_ID

            # Importing Required Models
            from app.blueprints.scan.models import ARP
            # Importing Required Models

            # Querying the Database
            arps = db.session.query(IPSegment, ARP).join(ARP, IPSegment.ip_segment_id == ARP.fk_ip_address_id).filter(
                IPSegment.fk_router_id == fk_router_id  # ARP Router ID
            ).all()
            # Querying the Database

            # For each ARP in the Database
            for ip, arp in arps:
                # If the ARP is not in the router list
                if str(arp.arp_ip) + "@" + str(arp.arp_mac) not in router_arp_list_p:
                    db.session.delete(arp)  # Delete the ARP
        except Exception as e:  # If an Exception occurs
            print("Error in delete_arps: " + str(e))  # Print the Exception
    # Function to delete ARPs that are in the database but are not in the router list

    # Function to detect if IP is duplicated with at least one MAC and change the ARP Tag to IP_ADDRESS_DUPLICATED
    @staticmethod
    def detect_ip_duplicated():
        try:
            # Importing Required Models
            from app.blueprints.scan.models import ARP
            # Importing Required Models

            # Querying only the id and IP from the Database
            arps = ARP.query.with_entities(ARP.arp_id, ARP.arp_ip).all()
            # Querying only the id and IP from the Database

            # Counting the IPs
            arp_ip_count = Counter([arp.arp_ip for arp in arps])
            # Counting the IPs

            # For each IP in the ARP IP Count
            for item, count in arp_ip_count.items():
                # If the IP is duplicated
                if count > 1:
                    # For each ARP in the ARPs
                    for arp in arps:
                        # If the ARP IP is equal to the IP
                        if arp.arp_ip == item:
                            array = json.loads(arp.arp_tag)
                            array.append(ARPTag.IP_ADDRESS_DUPLICATED)  # Add the IP Address Duplicated Tag
                            arp.arp_tag = json.dumps(array)  # Update the ARP Tag
            # For each ARP in the ARPs

            db.session.commit()  # Commit the Database Session
        except Exception as e:  # If an Exception occurs
            print(str(e))  # Print the Exception
    # Function to detect if IP is duplicated with at least one MAC and change the ARP Tag to IP_ADDRESS_DUPLICATED

    # Function to assign the alias to the ARP based on the Queue List by JSON as parameter
    @staticmethod
    def assign_alias(arp_ip: str, queue_list: dict) -> str:
        try:
            # Importing Required Models
            from app.blueprints.scan.models import ARP
            # Importing Required Models

            # For each Queue in the Queue List
            for key, value in queue_list.items():
                if arp_ip == key:
                    return str(value)  # Return the Key
            else:
                return str("")  # Return an Empty String
            # For each Queue in the Queue List
        except Exception as e:
            print(str(e))  # Print the Exception
    # Function to assign the alias to the ARP based on the Queue List by JSON as parameter
