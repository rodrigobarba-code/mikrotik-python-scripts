from api.routeros.modules.ip_address import IPAddress

class RouterAPI:
    @staticmethod
    async def arp_scan():
        """
        ARP Scan
        :return: List of IP Addresses
        """
        ip_addresses_list = IPAddress()._obtain_all()
        IPAddress()._add_to_database(ip_addresses_list)
        print('ARP Scan Completed')
