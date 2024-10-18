from typing import List
from ...auth import verify_jwt
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request
from utils.threading_manager import ThreadingManager

from ...functions import APIFunctions
from entities.ip_groups import IPGroupsEntity
from models.ip_management.models import IPGroups

ip_groups_router = APIRouter()
ip_groups_functions = APIFunctions()

class IPGroupsBulkDeleteBase(BaseModel):
    ip_groups_ids: List[int]

class IPGroupsTagsBase(BaseModel):
    tags: List[int]

@ip_groups_router.get("/ip/groups/")
async def get_ip_groups(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(IPGroups.get_ip_groups, 'r')
            ip_groups = [
                {
                    'ip_group_id': ip_group.ip_group_id,
                    'fk_ip_segment_id': ip_group.fk_ip_segment_id,
                    'ip_group_name': ip_group.ip_group_name,
                    'ip_group_type': ip_group.ip_group_type,
                    'ip_group_alias': ip_group.ip_group_alias,
                    'ip_group_description': ip_group.ip_group_description,
                    'ip_group_ip': ip_group.ip_group_ip,
                    'ip_group_mask': ip_group.ip_group_mask,
                    'ip_group_mac': ip_group.ip_group_mac,
                    'ip_group_mac_vendor': ip_group.ip_group_mac_vendor,
                    'ip_group_interface': ip_group.ip_group_interface,
                    'ip_group_comment': ip_group.ip_group_comment,
                    'ip_is_dhcp': ip_group.ip_is_dhcp,
                    'ip_is_dynamic': ip_group.ip_is_dynamic,
                    'ip_is_complete': ip_group.ip_is_complete,
                    'ip_is_disabled': ip_group.ip_is_disabled,
                    'ip_is_published': ip_group.ip_is_published,
                    'ip_duplicity': ip_group.ip_duplicity,
                    'ip_duplicity_indexes': ip_group.ip_duplicity_indexes
                }
                for ip_group in request
            ]
            ip_groups_functions.create_transaction_log(
                action="GET",
                table="ip_groups",
                user_id=int(user_id),
                description="IP Groups table retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "IP Groups table retrieved successfully",
                'ip_groups': ip_groups,
                'length': len(ip_groups),
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve IP Groups table: {str(e)}",
            'backend_status': 400
        }

@ip_groups_router.get("/ip/group/{ip_group_id}")
async def get_ip_group(user_id: int, ip_group_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(IPGroups.get_ip_group, 'rx', ip_group_id)
            ip_group = {
                'ip_group_id': request.ip_group_id,
                'fk_ip_segment_id': request.fk_ip_segment_id,
                'ip_group_name': request.ip_group_name,
                'ip_group_type': request.ip_group_type,
                'ip_group_alias': request.ip_group_alias,
                'ip_group_description': request.ip_group_description,
                'ip_group_ip': request.ip_group_ip,
                'ip_group_mask': request.ip_group_mask,
                'ip_group_mac': request.ip_group_mac,
                'ip_group_mac_vendor': request.ip_group_mac_vendor,
                'ip_group_interface': request.ip_group_interface,
                'ip_group_comment': request.ip_group_comment,
                'ip_is_dhcp': request.ip_is_dhcp,
                'ip_is_dynamic': request.ip_is_dynamic,
                'ip_is_complete': request.ip_is_complete,
                'ip_is_disabled': request.ip_is_disabled,
                'ip_is_published': request.ip_is_published,
                'ip_duplicity': request.ip_duplicity,
                'ip_duplicity_indexes': request.ip_duplicity_indexes
            }
            ip_groups_functions.create_transaction_log(
                action="GET",
                table="ip_groups",
                user_id=int(user_id),
                description=f"IP Group {ip_group_id} retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': f"IP Group {ip_group_id} retrieved successfully",
                'ip_group': ip_group,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve IP Group {ip_group_id}: {str(e)}",
            'backend_status': 400
        }

@ip_groups_router.put("/ip/group/{ip_group_id}")
async def update_ip_group(user_id: int, ip_group_id: int, tags: IPGroupsTagsBase, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_functions.verify_user_existence(user_id):
            ip_group_metadata = {'ip_group_id': ip_group_id, 'tags': tags.tags}
            ThreadingManager().run_thread(IPGroups.update_ip_group, 'w', ip_group_metadata)
            ip_groups_functions.create_transaction_log(
                action="UPDATE",
                table="ip_groups",
                user_id=int(user_id),
                description=f"IP Group {ip_group_id} updated successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': f"IP Group {ip_group_id} updated successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to update IP Group {ip_group_id}: {str(e)}",
            'backend_status': 400
        }