from api.routeros.modules.ip_address import IPAddress
from api.routeros.modules.arp import ARP

class RouterAPI:
    @staticmethod
    async def arp_scan():
        ip_addresses_list = IPAddress().obtain_all()
        IPAddress().add_to_database(ip_addresses_list)

        arp_list = ARP().obtain_all()
        response = ARP().add_to_database(arp_list)

        print(f'ARP Scan: {response}')
