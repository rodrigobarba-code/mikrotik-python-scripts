from api.routeros.modules.arp import ARP
from api.routeros.modules.ip_address import IPAddress
from api.routeros.modules.pdf_generator import PDFGenerator as pdf

class RouterAPI:
    @staticmethod
    async def arp_scan():
        # Obtain all IP addresses
        ip_addresses_list = IPAddress().obtain_all()
        # Add IP addresses to the database
        IPAddress().add_to_database(ip_addresses_list)

        # Obtain all ARP entries
        arp_list = ARP().obtain_all()
        # Obtain the last ARP entries since the last scan
        response_old: list = ARP().obtain_last_data()
        # Add ARP entries to the database
        response_new: dict = ARP().add_to_database(arp_list)

        # Generate a scan report
        scan_report_pdf = pdf()
        # Give the metadata to the PDF generator
        scan_report_pdf.generate_scan_report({
            'annomalies': {
                'ip_annomalies': [],
                'mac_annomalies': []
            },
            'old_data': response_old if response_old else None,
            'new_data': {
                'added': response_new['added'] if response_new['added'] else None,
                'updated': response_new['updated'] if response_new['updated'] else None,
                'deleted': response_new['deleted'] if response_new['deleted'] else None
            }
        })

        # Return the ARP scan response
        print(f'ARP Scan: {response_new['size']}')
