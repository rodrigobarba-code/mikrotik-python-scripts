import api.routeros.modules.routeros_object as ro  # RouterOS Object
from models.routers.models import Router as r  # Router Model
from utils.threading_manager import ThreadingManager as tm  # Threading Manager


# AllowedRouters Class
class AllowedRouters(ro.RouterOSObject):
    id : int = None  # Router ID
    router : object = None  # Router Model

    def __init__(self, id=None, host=None, username=None, password=None, port=None, ssl=None):
        """
        Constructor for AllowedRouters
        :param host: IP Address or Hostname
        :param username: Username
        :param password: Password
        :param port: Port
        :param ssl: Use SSL
        """
        super().__init__(host, username, password, port, ssl)
        self.id = id
        self.router = super().get()

    def get(self) -> object:
        """
        Get Router Model
        :return: Router Model
        """
        return self.router

    @staticmethod
    def get_all() -> list[object]:
        """
        Get all allowed routers
        :return: List of AllowedRouters
        """

        router_list = []  # List of AllowedRouters

        # Get all routers
        for router in tm().run_thread(r.get_routers, 'r'):
            # Append to router_list
            if router.allow_scan == 1:
                router_list.append(
                    # AllowedRouters Object
                    AllowedRouters(
                        id=router.router_id,  # Router ID
                        host=router.router_ip,  # IP Address or Hostname
                        username=router.router_username,  # Username
                        password=router.router_password,  # Password
                        port=7372,  # Port
                        ssl=True  # Use SSL
                    )
                )

        return router_list  # Return router_list

    def __str__(self):
        """
        String representation of AllowedRouters
        :return: String
        """
        return f"<AllowedRouters: {self.host}>"

    def __repr__(self):
        """
        Representation of AllowedRouters
        :return: String
        """
        return f"<AllowedRouters: {self.host}>"
