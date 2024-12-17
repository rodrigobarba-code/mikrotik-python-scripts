import api.routeros.modules.allowed_routers as ar
import entities.ip_segment as ips
from models.ip_management.models import IPSegment
from utils.threading_manager import ThreadingManager as tm


class IPAddress:
    ip_address_list = []

    def __init__(self):
        pass

    @staticmethod
    def _obtain_all() -> list[ips.IPSegmentEntity]:
        ip_addresses_list = []

        for router in ar.AllowedRouters.get_all():
            response = router.talk('/ip/address/print')

            for ip_address in response:
                if 'comment' in ip_address:
                    comment = ip_address['comment']
                else:
                    comment = ''

                tag = ''
                if ip_address['address'].startswith('10.'):
                    tag += 'Private,'
                else:
                    tag += 'Public,'

                if ip_address['interface'] == 'bridgeAPs':
                    tag += 'Main Interface,'
                else:
                    tag += 'Other Interface,'

                if ip_address['dynamic'] == 'true':
                    tag += 'Dynamic,'
                else:
                    tag += 'Static,'

                if ip_address['invalid'] == 'true':
                    tag += 'Not Used,'
                else:
                    tag += 'Used,'

                if 'comment' not in ip_address:
                    tag += 'No Commented,'
                else:
                    tag += 'Commented,'


                ip_segment = ips.IPSegmentEntity(
                    ip_segment_id=int(),
                    fk_router_id=router.id,
                    ip_segment_ip=ip_address['address'].split('/')[0],
                    ip_segment_mask=ip_address['address'].split('/')[1],
                    ip_segment_network=ip_address['network'],
                    ip_segment_interface=ip_address['interface'],
                    ip_segment_actual_iface=ip_address['actual-interface'],
                    ip_segment_tag=tag,
                    ip_segment_comment=comment,
                    ip_segment_is_invalid=True if ip_address['invalid'] == 'true' else False,
                    ip_segment_is_dynamic=True if ip_address['dynamic'] == 'true' else False,
                    ip_segment_is_disabled=True if ip_address['disabled'] == 'true' else False
                )

                ip_segment.validate_ip_segment()

                if ip_segment.ip_segment_is_disabled is False:
                    ip_addresses_list.append(ip_segment)
        return ip_addresses_list

    @staticmethod
    def _add_to_database(ip_addresses_list: list[ips.IPSegmentEntity]):
        try:
            tm().run_thread(IPSegment.bulk_add_ip_segments, 'w', ip_addresses_list)
        except Exception as e:
            print(e)
