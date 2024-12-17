import entities.ip_groups as ipg
from models.ip_management.models import IPGroups
from api.routeros.modules.ip_address import IPAddress
from api.routeros.modules.queue_list import QueueList
from utils.threading_manager import ThreadingManager as tm
from api.routeros.modules.allowed_routers import AllowedRouters


class ARP(QueueList, IPAddress):
    def __init__(self):
        pass

    @staticmethod
    def obtain_all() -> list[ipg.IPGroupsEntity]:
        ip_groups_list = []

        for router in AllowedRouters.get_all():
            response = router.talk('/ip/arp/print')
            oui_database = ARP._load_oui_database()
            queue_list = QueueList()._obtain_by_router(router)
            ip_segments = IPAddress()._get_segments_by_router(router.id)

            for arp in response:
                segment_metadata = IPAddress()._resolve_ip_segment(ip_segments, arp['address'])

                if 'comment' in arp:
                    comment = arp['comment']
                else:
                    comment = 'No Comment'

                if segment_metadata[0]:
                    if arp['interface'] == 'bridgeAPs':
                        ip_group = ipg.IPGroupsEntity(
                            ip_group_id=int(),
                            fk_ip_segment_id=segment_metadata[1],
                            ip_group_name='connected',
                            ip_group_type='private' if arp['address'].startswith('10.') else 'public',
                            ip_group_alias=QueueList()._get_alias(arp['address'], queue_list),
                            ip_group_description='No Description',
                            ip_group_ip=arp['address'],
                            ip_group_mask=str(segment_metadata[2]),
                            ip_group_mac=arp['mac-address'] if 'mac-address' in arp else 'No MAC',
                            ip_group_mac_vendor=ARP._get_mac_vendor(
                                arp['mac-address'] if 'mac-address' in arp else '00:00:00:00:00:00', oui_database),
                            ip_group_interface=arp['interface'],
                            ip_group_comment=comment,
                            ip_is_dhcp=True if arp['dynamic'] == 'true' else False,
                            ip_is_dynamic=True if arp['dynamic'] == 'true' else False,
                            ip_is_complete=True if arp['complete'] == 'true' else False,
                            ip_is_disabled=True if arp['disabled'] == 'true' else False,
                            ip_is_published=True if arp['published'] == 'true' else False,
                            ip_duplicity=False,
                            ip_duplicity_indexes=""
                        )

                        ip_group.validate_ip_group()

                        ip_groups_list.append(ip_group)

        return ip_groups_list

    @staticmethod
    def add_to_database(ip_groups_list: list[ipg.IPGroupsEntity]):
        try:
            tm().run_thread(IPGroups.bulk_add_ip_groups, 'w', ip_groups_list)
        except Exception as e:
            print(f'Error on _add_to_database: {e}')

    @staticmethod
    def _load_oui_database(file_path='api/routeros/modules/oui.txt') -> dict:
        oui_dict = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if "(base 16)" in line:
                        clean_line = " ".join(line.split()).strip()
                        oui, vendor = clean_line.split("(base 16)", 1)
                        oui = oui.strip().replace("-", ":")
                        vendor = vendor.strip()
                        oui_dict[oui] = vendor
        except FileNotFoundError:
            print(f"Error: Archivo no encontrado en la ruta '{file_path}'.")
        except Exception as e:
            print(f"Error al cargar la base de datos OUI: {e}")
        return oui_dict

    @staticmethod
    def _get_mac_vendor(mac_address, oui_dict):
        mac_prefix = mac_address.upper().replace(":", "")[:6]
        return oui_dict.get(mac_prefix, "Unknown") if mac_address != "00:00:00:00:00:00" else "Unknown"
