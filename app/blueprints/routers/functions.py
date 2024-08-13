# Importing Necessary Libraries
import re
import ipaddress
from app.extensions import func
# Importing Necessary Libraries

# Importing Required Exceptions
from app.blueprints.routers.exceptions import *
# Importing Required Exceptions

# Class for Routers Functions
class RoutersFunctions:
    # Constructor
    def __init__(self):  # Constructor
        pass  # Pass the constructor
    # Constructor

    # Function to validate the Router IP
    @staticmethod
    def validate_ip(ip):
        try:
            ipaddress.ip_address(ip)  # Validate the IP Address
            return True  # Return True
        except ValueError:
            return False  # Return False
    # Function to validate the Router IP

    # Function to validate the Router MAC
    @staticmethod
    def validate_mac(mac):
        try:
            # Check if the MAC Address is correct
            if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
                return True  # Return True
            else:
                return False  # Return False
        except ValueError:
            return False  # Return False
    # Function to validate the Router MAC

    # Function to validate the all the Router details
    @staticmethod
    def validate_router(router, operation, model) -> bool:
        try:
            if operation in ["insert", "update"]:  # Check if the operation is insert or update
                if operation == "update":  # If the operation is updated
                    existing_router = model.query.get(router.router_id)  # Get the existing router
                    if not existing_router:  # Check if the existing router is not found
                        raise RouterNotFound(router.router_id)  # Raise Router Not Found Exception
                # Check if the router name is empty
                if model.query.filter(func.lower(model.router_name) == func.lower(router.router_name)).first() and \
                        model.query.filter(func.lower(model.router_name) == func.lower(router.router_name)).first().router_id != router.router_id:
                    raise RouterAlreadyExists(  # Raise Router Already Exists Exception
                        router_id=model.query.filter(  # Get the router id
                            func.lower(model.router_name) == func.lower(router.router_name)).first().router_id,
                        router_name=router.router_name  # Get the router name
                    )
                # Check if the router IP is valid
                if not RoutersFunctions.validate_ip(router.router_ip):
                    raise RouterIPNotValid(router.router_ip)  # Raise Router IP Not Valid Exception
                # Check if the router MAC is valid
                if not RoutersFunctions.validate_mac(router.router_mac):
                    raise RouterMACNotValid(router.router_mac)  # Raise Router MAC Not Valid Exception
                # Check if the router IP already exists
                if model.query.filter(func.lower(model.router_ip) == func.lower(router.router_ip)).first() and \
                        model.query.filter(func.lower(model.router_ip) == func.lower(router.router_ip)).first().router_id != router.router_id:
                    raise RouterIPAlreadyExists(  # Raise Router IP Already Exists Exception
                        router_id=model.query.filter(  # Get the router id
                            func.lower(model.router_ip) == func.lower(router.router_ip)).first().router_id,
                        router_ip=router.router_ip  # Get the router IP
                    )
                # Check if the router MAC already exists
                if model.query.filter(func.lower(model.router_mac) == func.lower(router.router_mac)).first() and \
                        model.query.filter(func.lower(model.router_mac) == func.lower(router.router_mac)).first().router_id != router.router_id:
                    raise RouterMACAlreadyExists(  # Raise Router MAC Already Exists Exception
                        router_id=model.query.filter(  # Get the router id
                            func.lower(model.router_mac) == func.lower(router.router_mac)).first().router_id,
                        router_mac=router.router_mac  # Get the router MAC
                    )
                return True  # Return True
            # Check if the operation is deleted or get
            elif operation in ["delete", "get"]:  # If the operation is deleted or get
                if not model.query.filter(model.router_id == router.router_id).first():  # Check if the router id is not found
                    raise RouterNotFound(router.router_id)  # Raise Router Not Found Exception
                return True  # Return True
            return False  # Return False if the operation is not found
        except (RouterNotFound, RouterIPNotValid, RouterMACNotValid, RouterAlreadyExists, RouterIPAlreadyExists,
                RouterMACAlreadyExists) as e:  # Catch the exceptions
            raise e  # Raise the exception
        except Exception:  # Catch the exception
            raise RouterError()  # Raise Router Error Exception
    # Function to validate the all the Router details
# Class for Routers Functions
