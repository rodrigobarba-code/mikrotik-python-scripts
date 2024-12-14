# Import RouterOS API for Mikrotik
import ros_api as routeros_api

# Class RouterOSObject
class RouterOSObject:
    host : str = None  # Hostname or IP Address
    username : str = None  # Username
    password : str = None  # Password
    port : int = 7372  # Default port for RouterOS API
    ssl : bool = True  # Use SSL

    api : object = None  # RouterOS API Object

    def __init__(self, host=None, username=None, password=None, port=None, ssl=None):
        """
        Constructor for RouterOSObject
        :param host: IP Address or Hostname
        :param username: Username
        :param password: Password
        :param port: Port
        :param ssl: Use SSL
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.ssl = ssl

        self.api = routeros_api.Api(
            address=self.host,
            user=self.username,
            password=self.password,
            port=self.port,
            use_ssl=self.ssl
        )

    def get(self) -> object:
        """
        Get RouterOS API Object
        :return: RouterOS API Object
        """
        return self.api

    def set(self, host=None, username=None, password=None, port=None, ssl=None):
        """
        Set RouterOS API Object
        :param host: IP Address or Hostname
        :param username: Username
        :param password: Password
        :param port: Port
        :param ssl: Use SSL
        :return:
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.ssl = ssl

        self.api = routeros_api.Api(
            address=self.host,
            user=self.username,
            password=self.password,
            port=self.port,
            use_ssl=self.ssl
        )

    def __str__(self):
        """
        String representation of RouterOSObject
        :return: String
        """
        return f"<RouterOSObject: {self.host}, {self.username}, {self.password}, {self.port}, {self.ssl}>"

    def __repr__(self):
        """
        Representation of RouterOSObject
        :return: String
        """
        return f"<RouterOSObject: {self.host}, {self.username}, {self.password}, {self.port}, {self.ssl}>"

    def talk(self, command: str):
        """
        Talk to RouterOS (Send one command)
        :param command: Command to send
        :return: Response
        """
        return self.api.talk(command)

    def communicate(self, command: list[str]):
        """
        Communicate with RouterOS (Send multiple commands)
        :param command: List of commands
        :return: Response
        """
        return self.api.communicate(command)
