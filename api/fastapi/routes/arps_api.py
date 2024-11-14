from typing import List
from ...auth import verify_jwt
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request
from utils.threading_manager import ThreadingManager

from ...functions import APIFunctions
from models.router_scan.models import ARP
# from models.router_scan.models import ARPTags

arps_router = APIRouter()
arps_functions = APIFunctions()

class ARPBulkDeleteBase(BaseModel):
    arps_ids: List[int]

@arps_router.get("/arps/")
async def get_arps(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if arps_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(ARP.get_arps, 'r')
            arps = [
                {
                    "arp_id": arp.arp_id,
                    "fk_ip_address_id": arp.fk_ip_address_id,
                    "arp_ip": arp.arp_ip,
                    "arp_mac": arp.arp_mac,
                    "arp_alias": arp.arp_alias,
                    "arp_interface": arp.arp_interface,
                    "arp_is_dhcp": arp.arp_is_dhcp,
                    "arp_is_invalid": arp.arp_is_invalid,
                    "arp_is_dynamic": arp.arp_is_dynamic,
                    "arp_is_complete": arp.arp_is_complete,
                    "arp_is_disabled": arp.arp_is_disabled,
                    "arp_is_published": arp.arp_is_published
                }
                for arp in request
            ]
            arps_functions.create_transaction_log(
                action="GET",
                table="arps",
                user_id=int(user_id),
                description="ARP table retrieved",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "ARP table retrieved successfully",
                'arps': arps,
                'lenght': len(arps),
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve ARP table: {str(e)}",
            'backend_status': 400
        }

@arps_router.get("/arps/essential/")
async def get_arps_essential(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    from models import SessionLocal
    try:
        arps = []
        if arps_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(ARP.get_arps, 'r')

            for arp in request:
                session_for_segment = SessionLocal()
                session_for_tags = SessionLocal()
                arp = {
                    'id': arp.arp_id,
                    'ip': arp.arp_ip,
                    'mac': arp.arp_mac,
                    'segment': ARP.get_segment(session_for_segment, arp.fk_ip_address_id),
                    'interface': arp.arp_interface,
                    'alias': arp.arp_alias,
                    'tag': [arp.arp_tag]
                }
                arps.append(arp)
                session_for_segment.close()
                session_for_tags.close()

            arps_functions.create_transaction_log(
                action="GET",
                table="arps",
                user_id=int(user_id),
                description="ARP essential table retrieved",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "ARP essential table retrieved successfully",
                'arps': arps,
                'length': len(arps),
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve ARP essential table: {str(e)}",
            'backend_status': 400
        }

@arps_router.get("/arp/essential/{arp_id}")
async def get_arp_essential(user_id: int, metadata: Request, arp_id: str, token: dict = Depends(verify_jwt)):
    from models import SessionLocal
    try:
        if arps_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(ARP.get_arp, 'rx', arp_id)

            session_for_segment = SessionLocal()
            session_for_tags = SessionLocal()
            arp = {
                'id': request.arp_id,
                'ip': request.arp_ip,
                'mac': request.arp_mac,
                'segment': ARP.get_segment(session_for_segment, request.fk_ip_address_id),
                'interface': request.arp_interface,
                'alias': request.arp_alias,
                'tag': [request.arp_tag],
                'is_dhcp': request.arp_is_dhcp,
                'is_invalid': request.arp_is_invalid,
                'is_dynamic': request.arp_is_dynamic,
                'is_complete': request.arp_is_complete,
                'is_disabled': request.arp_is_disabled,
                'is_published': request.arp_is_published
            }
            session_for_segment.close()
            session_for_tags.close()

            arps_functions.create_transaction_log(
                action="GET",
                table="arp",
                user_id=int(user_id),
                description="ARP essential retrieved",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "ARP essential retrieved successfully",
                'arp': arp,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve ARP essential: {str(e)}",
            'backend_status': 400
        }

@arps_router.get("/arp/{arp_id}")
async def get_arp(user_id: int, metadata: Request, arp_id: int, token: dict = Depends(verify_jwt)):
    try:
        if arps_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(ARP.get_arp, 'rx', arp_id)
            arp = {
                "arp_id": request.arp_id,
                "fk_ip_address_id": request.fk_ip_address_id,
                "arp_ip": request.arp_ip,
                "arp_mac": request.arp_mac,
                "arp_alias": request.arp_alias,
                "arp_tag": request.arp_tag,
                "arp_interface": request.arp_interface,
                "arp_is_dhcp": request.arp_is_dhcp,
                "arp_is_invalid": request.arp_is_invalid,
                "arp_is_dynamic": request.arp_is_dynamic,
                "arp_is_complete": request.arp_is_complete,
                "arp_is_disabled": request.arp_is_disabled,
                "arp_is_published": request.arp_is_published
            }
            arps_functions.create_transaction_log(
                action="GET",
                table="arp",
                user_id=int(user_id),
                description="ARP retrieved",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "ARP retrieved successfully",
                'arp': arp,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve ARP: {str(e)}",
            'backend_status': 400
        }

@arps_router.delete("/arps/")
async def delete_arps(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if arps_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(ARP.delete_all_arps, 'wx')
            ThreadingManager().run_thread(ARP.verify_autoincrement_id, 'r')
            arps_functions.create_transaction_log(
                action="DELETE",
                table="arps",
                user_id=int(user_id),
                description="ARP table deleted",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "ARP table deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete ARP table: {str(e)}",
            'backend_status': 400
        }

@arps_router.delete("/arp/{arp_id}")
async def delete_arp(user_id: int, metadata: Request, arp_id: str, token: dict = Depends(verify_jwt)):
    try:
        if arps_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(ARP.delete_arp, 'w', arp_id)
            ThreadingManager().run_thread(ARP.verify_autoincrement_id, 'r')
            arps_functions.create_transaction_log(
                action="DELETE",
                table="arp",
                user_id=int(user_id),
                description="ARP deleted",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "ARP deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete ARP: {str(e)}",
            'backend_status': 400
        }

@arps_router.delete("/arps/bulk/")
async def bulk_delete_arps(user_id: int, metadata: Request, request: ARPBulkDeleteBase, token: dict = Depends(verify_jwt)):
    try:
        if arps_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(ARP.bulk_delete_arps, 'w', request.arps_ids)
            ThreadingManager().run_thread(ARP.verify_autoincrement_id, 'r')
            arps_functions.create_transaction_log(
                action="DELETE",
                table="arps",
                user_id=int(user_id),
                description="ARP table deleted",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "ARP table deleted successfully",
                'backend_status': 200,
                'count_flag': len(request.arps_ids)
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete ARP table: {str(e)}",
            'backend_status': 400,
        }
