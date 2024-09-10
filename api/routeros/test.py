import ros_api
connection = ros_api.Api('10.1.3.254', 'AccesoN0C','N0c#2024.@!!', port=7372,  use_ssl=True)
def run_arp_print(connection):
    try:
        response = connection.talk(['/queue/simple/print'])
        for item in response:
            print(item)
    except Exception as e:
        print(f"Error running /ip/arp/print: {e}")
    finally:
        connection.close()

run_arp_print(connection)
