from ...auth import verify_jwt
from fastapi import APIRouter, Depends, Request
from utils.threading_manager import ThreadingManager

from ...functions import APIFunctions
from models.router_scan.models import ARPTags

arptags_router = APIRouter()
arptags_functions = APIFunctions()

@arptags_router.get("/arp/{arp_id}/tags")
async def get_arp_tags(user_id: int, metadata: Request, arp_id: int, token: dict = Depends(verify_jwt)):
    try:
        if arptags_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(ARPTags.get_arp_tags, 'rx', arp_id)
            arp_tags = request
            arptags_functions.create_transaction_log(
                action="GET",
                table="arp_tags",
                user_id=int(user_id),
                description="ARP tags retrieved",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "ARP tags retrieved successfully",
                'arp_tags': arp_tags,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve ARP tags: {str(e)}",
            'backend_status': 400
        }

@arptags_router.delete("/arp/{arp_id}/tags")
async def delete_arp_tags(user_id: int, metadata: Request, arp_id: int, token: dict = Depends(verify_jwt)):
    try:
        if arptags_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(ARPTags.delete_arp_tags, 'w', arp_id)
            arptags_functions.create_transaction_log(
                action="DELETE",
                table="arp_tags",
                user_id=int(user_id),
                description="ARP tags deleted",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "ARP tags deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete ARP tags: {str(e)}",
            'backend_status': 400
        }

@arptags_router.delete("/arp/tag/{arp_tag_id}")
async def delete_arp_tag(user_id: int, metadata: Request, arp_tag_id: int, token: dict = Depends(verify_jwt)):
    try:
        if arptags_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(ARPTags.delete_arp_tag, 'w', arp_tag_id)
            arptags_functions.create_transaction_log(
                action="DELETE",
                table="arp_tags",
                user_id=int(user_id),
                description="ARP tag deleted",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "ARP tag deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete ARP tag: {str(e)}",
            'backend_status': 400
        }

@arptags_router.delete("/arp/tags/")
async def delete_all_arp_tags(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if arptags_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(ARPTags.delete_all_arp_tags, 'wx')
            arptags_functions.create_transaction_log(
                action="DELETE",
                table="arp_tags",
                user_id=int(user_id),
                description="All ARP tags deleted",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "All ARP tags deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete all ARP tags: {str(e)}",
            'backend_status': 400
        }
