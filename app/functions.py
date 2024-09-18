import os
import socket
import requests as r
from dotenv import load_dotenv

def get_public_ip():
    endpoint = 'https://ipinfo.io/json'  
    response = r.get(endpoint, verify=True)
    if response.status_code != 200:  
        return 'Status:', response.status_code, 'Problem with the request. Exiting.'
    data = response.json()  
    return data['ip']  

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip  
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_verified_jwt_header() -> dict:
    import json
    import http.client

    load_dotenv()

    conn = http.client.HTTPSConnection(os.getenv('APP_AUTH0_DOMAIN'))
    payload = "{\"client_id\":\"" + os.getenv('APP_AUTH0_CLIENT_ID') + "\",\"client_secret\":\"" + os.getenv('APP_AUTH0_CLIENT_SECRET') + "\",\"audience\":\"" + os.getenv('APP_AUTH0_AUDIENCE') + "\",\"grant_type\":\"client_credentials\"}"
    headers = {'content-type': "application/json"}
    conn.request("POST", "/oauth/token", payload, headers)

    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))

    access_token = data['access_token']
    token_type = data['token_type']
    return {'Authorization': f'{token_type} {access_token}'}

functions = {
    'get_public_ip': get_public_ip,
    'get_jwt_token': get_verified_jwt_header,
    'get_local_ip': get_local_ip,
}

if __name__ == '__main__':
    print(get_public_ip())
    print(get_local_ip())
    print(get_verified_jwt_header())