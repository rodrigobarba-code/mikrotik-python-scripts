from ...auth import verify_jwt
from fastapi import APIRouter, Depends, Request
from utils.threading_manager import ThreadingManager

from ...functions import APIFunctions
from models.router_scan.models import ARP

arps_router = APIRouter()
arps_functions = APIFunctions()

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
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve ARP table: {str(e)}",
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
async def delete_arp(user_id: int, metadata: Request, arp_id: int, token: dict = Depends(verify_jwt)):
    try:
        if arps_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(ARP.delete_arp, 'rx', arp_id)
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