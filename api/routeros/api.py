import asyncio
import ros_api

from utils.threading_manager import ThreadingManager

from entities.arp import ARPEntity
from models.router_scan.models import ARP, ARPTags
from models.router_scan.functions import ARPFunctions

from entities.ip_segment import IPSegmentEntity
from models.ip_management.models import IPSegment
from models.ip_management.functions import IPAddressesFunctions

from api.routeros.modules.FindIPSegment import FindIPSegment
from api.routeros.modules.GetAllowedRouters import GetAllowedRouters

class RouterAPI:
    SCAN_STATUS = ['IDLE', 'IN PROGRESS']

    router = None  
    credentials = None
    scan_status = {'status': SCAN_STATUS[0]}

    def __init__(
        self,  
        host,  
        user,  
        password  
    ):
        self.router = None
        self.credentials = {
            'host': host,
            'user': user,
            'password': password
        }

    def get_credentials(self):
        return self.credentials  

    def set_credentials(
        self,  
        host=None,  
        user=None,  
        password=None  
    ):
        self.credentials = {  
            'host': host,
            'user': user,
            'password': password
        }

    def get_api(self):
        return self.router  

    def set_api(self):
        self.router = ros_api.Api(  
            self.credentials['host'],  
            self.credentials['user'],  
            self.credentials['password'],  
            port=7372,  
            use_ssl=True  
        )

    @staticmethod
    def retrieve_data(router, command) -> dict:
        return router.talk(command)

    async def talk_with_timeout(router, command) -> dict:
        return await router.talk(command)

    async def verify_router_connection(router) -> bool:
        try:
            await asyncio.wait_for(RouterAPI.talk_with_timeout(router, '/system/identity/print'), timeout=10.0)
            return True
        except (Exception, asyncio.TimeoutError) as e:
            return False

    @staticmethod
    async def get_ip_data() -> list:
        ip_list = []

        routers = ThreadingManager().run_thread(GetAllowedRouters.get, 'r')

        for router in routers:
            router_api = RouterAPI(
                router.router_ip,
                router.router_username,
                router.router_password
            )
            router_api.set_api()

            router_id = router.router_id
            ip_data = RouterAPI.retrieve_data(router_api.get_api(), '/ip/address/print')

            for ip in ip_data:
                comment = "None"
                if 'comment' in ip:
                    comment = ip['comment']

                ip_tmp = ip['address'].split('/')

                ip_obj = IPSegmentEntity(
                    ip_segment_id=int(),
                    fk_router_id=router_id,
                    ip_segment_ip=ip_tmp[0],
                    ip_segment_mask=ip_tmp[1],
                    ip_segment_network=ip['network'],
                    ip_segment_interface=ip['interface'],
                    ip_segment_actual_iface=ip['actual-interface'],
                    ip_segment_tag=IPAddressesFunctions.determine_ip_segment_tag(ip_tmp[0]),
                    ip_segment_comment=comment,
                    ip_segment_is_invalid=True if ip['invalid'] == 'true' else False,
                    ip_segment_is_dynamic=True if ip['dynamic'] == 'true' else False,
                    ip_segment_is_disabled=True if ip['disabled'] == 'true' else False
                )

                ip_obj.validate_ip_segment()
                ip_list.append(ip_obj)

            ip_data = {'ip_list': ip_list, 'router_id': router.router_id}
            ThreadingManager().run_thread(IPAddressesFunctions.delete_ip_segments, 'w', ip_data)
        return ip_list

    @staticmethod
    def add_ip_data(ip_list: list[IPSegmentEntity]) -> None:
        try:
            for ip in ip_list:
                ip.validate_ip_segment()
            ThreadingManager().run_thread(IPSegment.bulk_add_ip_segments, 'w', ip_list)
        except Exception as e:  
            raise str('Error on adding IP data: ' + str(e))

    @staticmethod
    async def get_arp_data() -> list:
        arp_list = []

        routers = ThreadingManager().run_thread(GetAllowedRouters.get, 'r')

        for router in routers:  
            router_api = RouterAPI(  
                router.router_ip,  
                router.router_username,  
                router.router_password  
            )
            router_api.set_api()

            arp_region_list = []
            router_id = router.router_id  
            ip_segments_by_router = ThreadingManager().run_thread(IPSegment.get_ip_segments_by_router_id, 'rx', router_id)
            arp_data = RouterAPI.retrieve_data(router_api.get_api(), '/ip/arp/print')

            queue_dict = {}
            queue_data = RouterAPI.retrieve_data(router_api.get_api(), '/queue/simple/print')
            for queue in queue_data:
                name = queue['name']
                ip = queue['target'].split('/')[0]
                queue_dict[ip] = name

            for arp in arp_data:
                ip_segment = FindIPSegment.find(ip_segments_by_router, arp['address'])
                if ip_segment[0] is True:  
                    arp_obj = ARPEntity(  
                        arp_id=int(),  
                        fk_ip_address_id=int(ip_segment[1]),  
                        arp_ip=arp['address'],  
                        arp_mac="" if 'mac-address' not in arp else arp['mac-address'],  
                        arp_alias=ARPFunctions.assign_alias(str(arp['address']), queue_dict),
                        arp_interface=arp['interface'],  
                        arp_is_dhcp=True if arp['dynamic'] == 'true' else False,  
                        arp_is_invalid=True if arp['invalid'] == 'true' else False,  
                        arp_is_dynamic=True if arp['dynamic'] == 'true' else False,  
                        arp_is_complete=True if arp['complete'] == 'true' else False,  
                        arp_is_disabled=True if arp['disabled'] == 'true' else False,  
                        arp_is_published=True if arp['published'] == 'true' else False  
                    )
                    arp_obj.validate_arp()
                    arp_region_list.append(arp_obj)  
                else:
                    pass

            router_metadata = {'arp_region_list': arp_region_list, 'router_id': router.router_id, 'model': ARPTags}
            ThreadingManager().run_thread(ARPFunctions.delete_arps, 'w', router_metadata)
            
            arp_list.extend(arp_region_list)  
        return arp_list

    @staticmethod
    def add_arp_data(arp_list: list[ARPEntity]) -> None:
        try:
            for arp in arp_list:
                arp.validate_arp()
            ThreadingManager().run_thread(ARP.bulk_add_arp, 'w', arp_list)
            ThreadingManager().run_thread(ARPTags.assign_first_tag, 'wx')
        except Exception as e:  
            print(str('Error on adding ARP data: ' + str(e)))

    @staticmethod
    async def arp_scan():
        try:
            RouterAPI.scan_status = {'status': RouterAPI.SCAN_STATUS[1]}

            ip_data = await RouterAPI.get_ip_data()
            RouterAPI.add_ip_data(ip_data)
            arp_data = await RouterAPI.get_arp_data()
            RouterAPI.add_arp_data(arp_data)

            RouterAPI.scan_status = {'status': RouterAPI.SCAN_STATUS[0]}
        except Exception as e:
            raise e
