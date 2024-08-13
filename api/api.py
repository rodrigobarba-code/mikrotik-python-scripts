# Import the RouterOS API
import ros_api
# Import the RouterOS API

# Class to handle the RouterOS API
class RouterOSAPI:
    router = None  # RouterOS API object
    credentials = None  # RouterOS credentials

    # Constructor
    def __init__(self, host, user, password):
        self.credentials = {
            'host': host,
            'user': user,
            'password': password
        }
    # Constructor

    # Getters and Setters
    # Method to get the credentials
    def get_credentials(self):
        return self.credentials
    # Method to get the credentials

    # Method to set the credentials
    def set_credentials(self, host=None, user=None, password=None):
        self.credentials = {
            'host': host,
            'user': user,
            'password': password
        }
    # Method to set the credentials

    # Method to get the API object
    def get_api(self):
        return self.router
    # Method to get the API object

    # Method to set the API object
    def set_api(self):
        self.router = ros_api.Api(
            self.credentials['host'],
            self.credentials['user'],
            self.credentials['password'],
            port=7372,
            use_ssl=True
        )
    # Method to set the API object
    # Getters and Setters

    # Method to retrieve data from the RouterOS API
    def retrieve_data(self, command):
        self.set_api()  # Set the API object
        return self.router.talk(command)  # Run command and return the result
    # Method to retrieve data from the RouterOS API
# Class to handle the RouterOS API
