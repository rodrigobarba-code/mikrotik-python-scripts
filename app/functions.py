# Importing Necessary Libraries
import socket
import requests as r
# Importing Necessary Libraries

# Get Public IP Address Function
def get_public_ip():
    endpoint = 'https://ipinfo.io/json'  # Endpoint to get the public IP address
    response = r.get(endpoint, verify=True)  # Send a GET request to the endpoint

    if response.status_code != 200:  # Check if the request was successful
        return 'Status:', response.status_code, 'Problem with the request. Exiting.'  # Return an error message

    data = response.json()  # Get the JSON data from the response
    return data['ip']  # Return the public IP address
# Get Public IP Address Function

# Get Local IP Address Function
def get_local_ip():
    return socket.gethostbyname(socket.gethostname())  # Return the local IP address
# Get Local IP Address Function

# Create object for global functions
functions = {
    'get_public_ip': get_public_ip,  # Get the public IP address
    'get_local_ip': get_local_ip  # Get the local IP address
}
# Create object for global functions
