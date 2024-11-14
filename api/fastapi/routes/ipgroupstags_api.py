from ...auth import verify_jwt
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request
from utils.threading_manager import ThreadingManager

from ...functions import APIFunctions
from entities.ip_groups import IPGroupsTagsEntity
from models.ip_management.models import IPGroupsTags

ip_groups_tags_router = APIRouter()
ip_groups_tags_functions = APIFunctions()

class TagsBulkDeleteBase(BaseModel):
    tags_ids: list[int]

@ip_groups_tags_router.get("/ip/groups/tags/")
async def get_ip_groups_tags(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_tags_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(IPGroupsTags.get_ip_group_tags, 'r')
            ip_groups_tags = [
                {
                    'ip_group_tag_id': tag.ip_group_tag_id,
                    'ip_group_tag_name': tag.ip_group_tag_name,
                    'ip_group_tag_color': tag.ip_group_tag_color,
                    'ip_group_tag_text_color': tag.ip_group_tag_text_color,
                    'ip_group_tag_description': tag.ip_group_tag_description,
                }
                for tag in request
            ]
            ip_groups_tags_functions.create_transaction_log(
                action="GET",
                table="ip_groups_tags",
                user_id=int(user_id),
                description="IP Groups Tags table retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "IP Groups Tags table retrieved successfully",
                'ip_groups_tags': ip_groups_tags,
                'length': len(ip_groups_tags),
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve IP Groups table: {str(e)}",
            'backend_status': 400
        }

@ip_groups_tags_router.get("/ip/groups/tag/{ip_group_tag_id}")
async def get_ip_group_tag(user_id: int, ip_group_tag_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_tags_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(IPGroupsTags.get_ip_group_tag, 'rx', ip_group_tag_id)
            ip_group_tag = {
                'ip_group_tag_id': request.ip_group_tag_id,
                'ip_group_tag_name': request.ip_group_tag_name,
                'ip_group_tag_color': request.ip_group_tag_color,
                'ip_group_tag_text_color': request.ip_group_tag_text_color,
                'ip_group_tag_description': request.ip_group_tag_description,
            }
            ip_groups_tags_functions.create_transaction_log(
                action="GET",
                table="ip_groups_tags",
                user_id=int(user_id),
                description="IP Group Tag retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "IP Group Tag retrieved successfully",
                'ip_group_tag': ip_group_tag,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve IP Group Tag: {str(e)}",
            'backend_status': 400
        }

@ip_groups_tags_router.get("/ip/groups/tags/{ip_group_id}")
async def get_ip_group_tags_by_group_id(user_id: int, ip_group_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_tags_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(IPGroupsTags.get_tags_by_ip_group_id, 'rx', ip_group_id)
            ip_group_tags = [
                {
                    'ip_group_tag_id': tag.ip_group_tag_id,
                    'ip_group_tag_name': tag.ip_group_tag_name,
                    'ip_group_tag_color': tag.ip_group_tag_color,
                    'ip_group_tag_text_color': tag.ip_group_tag_text_color,
                    'ip_group_tag_description': tag.ip_group_tag_description,
                }
                for tag in request
            ]
            ip_groups_tags_functions.create_transaction_log(
                action="GET",
                table="ip_groups_tags",
                user_id=int(user_id),
                description="IP Group Tags retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "IP Group Tags retrieved successfully",
                'ip_group_tags': ip_group_tags,
                'length': len(ip_group_tags),
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve IP Group Tags: {str(e)}",
            'backend_status': 400
        }

@ip_groups_tags_router.post("/ip/groups/tag/")
async def add_ip_group_tag(
        user_id: int,
        metadata: Request,
        x_ip_group_tag_name: str,
        x_ip_group_tag_color: str,
        x_ip_group_tag_text_color: str,
        x_ip_group_tag_description: str,
        token: dict = Depends(verify_jwt)
):
    try:
        if ip_groups_tags_functions.verify_user_existence(user_id):
            ip_group_tag = IPGroupsTagsEntity(
                ip_group_tag_id=0,
                ip_group_tag_name=x_ip_group_tag_name,
                ip_group_tag_color=x_ip_group_tag_color,
                ip_group_tag_text_color=x_ip_group_tag_text_color,
                ip_group_tag_description=x_ip_group_tag_description,
            )
            ThreadingManager().run_thread(
                IPGroupsTags.add_ip_group_tag, 'w', ip_group_tag
            )
            ip_groups_tags_functions.create_transaction_log(
                action="POST",
                table="ip_groups_tags",
                user_id=int(user_id),
                description="IP Group Tag added successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "IP Group Tag added successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to add IP Group Tag: {str(e)}",
            'backend_status': 400
        }

@ip_groups_tags_router.put("/ip/groups/tag/{ip_group_tag_id}")
async def update_ip_group_tag(
        user_id: int,
        ip_group_tag_id: int,
        ip_group_tag_name: str,
        ip_group_tag_color: str,
        ip_group_tag_text_color: str,
        ip_group_tag_description: str,
        metadata: Request,
        token: dict = Depends(verify_jwt)
):
    try:
        if ip_groups_tags_functions.verify_user_existence(user_id):
            ip_group_tag = IPGroupsTagsEntity(
                ip_group_tag_id=ip_group_tag_id,
                ip_group_tag_name=ip_group_tag_name,
                ip_group_tag_color=ip_group_tag_color,
                ip_group_tag_text_color=ip_group_tag_text_color,
                ip_group_tag_description=ip_group_tag_description,
            )
            ThreadingManager().run_thread(
                IPGroupsTags.update_ip_group_tag, 'w', ip_group_tag
            )
            ip_groups_tags_functions.create_transaction_log(
                action="PUT",
                table="ip_groups_tags",
                user_id=int(user_id),
                description="IP Group Tag updated successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "IP Group Tag updated successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to update IP Group Tag: {str(e)}",
            'backend_status': 400
        }

@ip_groups_tags_router.delete("/ip/groups/tag/{ip_group_tag_id}")
async def delete_ip_group_tag(user_id: int, ip_group_tag_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_tags_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(IPGroupsTags.delete_ip_group_tag, 'w', ip_group_tag_id)
            ThreadingManager().run_thread(IPGroupsTags.verify_autoincrement_id, 'r')
            ip_groups_tags_functions.create_transaction_log(
                action="DELETE",
                table="ip_groups_tags",
                user_id=int(user_id),
                description="IP Group Tag deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "IP Group Tag deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete IP Group Tag: {str(e)}",
            'backend_status': 400
        }

@ip_groups_tags_router.delete("/ip/groups/tags/bulk/")
async def delete_ip_groups_tags_bulk(
        user_id: int,
        metadata: Request,
        request: TagsBulkDeleteBase,
        token: dict = Depends(verify_jwt)
):
    try:
        if ip_groups_tags_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(IPGroupsTags.bulk_delete_ip_group_tags, 'w', request.tags_ids)
            ThreadingManager().run_thread(IPGroupsTags.verify_autoincrement_id, 'r')
            ip_groups_tags_functions.create_transaction_log(
                action="DELETE",
                table="ip_groups_tags",
                user_id=int(user_id),
                description="IP Groups Tags bulk deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "IP Groups Tags bulk deleted successfully",
                'count_flag': len(request.tags_ids),
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete IP Groups Tags bulk: {str(e)}",
            'backend_status': 400
        }

@ip_groups_tags_router.delete("/ip/groups/tags/")
async def delete_ip_groups_tags(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_tags_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(IPGroupsTags.delete_ip_group_tags, 'wx')
            ThreadingManager().run_thread(IPGroupsTags.verify_autoincrement_id, 'r')
            ip_groups_tags_functions.create_transaction_log(
                action="DELETE",
                table="ip_groups_tags",
                user_id=int(user_id),
                description="IP Groups Tags table deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "IP Groups Tags table deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete IP Groups Tags table: {str(e)}",
            'backend_status': 400
        }