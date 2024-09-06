# Description: Module to get all allowed routers from the database.

# Importing necessary modules
from flask import current_app
# Importing necessary modules

# Importing Necessary Entities
from app.blueprints.routers.entities import RouterEntity
# Importing Necessary Entities

# Importing Necessary Modules
from app.blueprints.routers.models import Router
# Importing Necessary Modules

# Class to Get Allowed Routers
class GetAllowedRouters:
    # Constructor
    def __init__(
        self,  # Constructor
        db=None  # Database object
    ):
        self.db = db  # Setting the database object
    # Constructor

    # Method to Get Allowed Routers
    def get(self):
        try:  # Try to get the allowed routers
            with current_app.app_context():
                # Create a dictionary to store the routers
                routers_list = []
                # Querying the database for all allowed routers
                routers = self.db.session.query(Router).filter(Router.allow_scan == 1).all()
                # Loop through the routers
                for router in routers:
                    # Create a RouterEntity object
                    router_entity = RouterEntity(
                        router.router_id,  # Router ID
                        router.router_name,  # Router Name
                        router.router_description,  # Router Description
                        router.router_brand,  # Router Brand
                        router.router_model,  # Router Model
                        router.fk_site_id,  # Site ID
                        router.router_ip,  # Router IP
                        router.router_mac,  # Router MAC
                        router.router_username,  # Router Username
                        router.router_password,  # Router Password
                        router.allow_scan  # Allow Scan
                    )
                    # Add the router to the routers list
                    routers_list.append(router_entity)
                # Return the routers list
                return routers_list
        except Exception as e:  # Catch any exceptions
            # Return an error message
            return str("An error occurred while getting the allowed routers: " + str(e))
    # Method to Get Allowed Routers

# Class to Get Allowed Routers
