from typing import List

from entities.ip_groups import IPGroupsEntity
from ...auth import verify_jwt
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request
from utils.threading_manager import ThreadingManager

from ...functions import APIFunctions
from models.ip_management.models import IPGroups

ip_groups_router = APIRouter()
ip_groups_functions = APIFunctions()


class IPGroupsBulkDeleteBase(BaseModel):
    ip_groups_ids: List[int]


class BlacklistBulkMoveBase(BaseModel):
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
                    'ip_group_id': ip_group[0].ip_group_id,
                    'fk_ip_segment_id': ip_group[0].fk_ip_segment_id,
                    'ip_group_name': ip_group[0].ip_group_name,
                    'ip_group_type': ip_group[0].ip_group_type,
                    'ip_group_alias': ip_group[0].ip_group_alias,
                    'ip_group_description': ip_group[0].ip_group_description,
                    'ip_group_ip': ip_group[0].ip_group_ip,
                    'ip_group_mask': ip_group[0].ip_group_mask,
                    'ip_group_mac': ip_group[0].ip_group_mac,
                    'ip_group_mac_vendor': ip_group[0].ip_group_mac_vendor,
                    'ip_group_interface': ip_group[0].ip_group_interface,
                    'ip_group_comment': ip_group[0].ip_group_comment,
                    'ip_is_dhcp': ip_group[0].ip_is_dhcp,
                    'ip_is_dynamic': ip_group[0].ip_is_dynamic,
                    'ip_is_complete': ip_group[0].ip_is_complete,
                    'ip_is_disabled': ip_group[0].ip_is_disabled,
                    'ip_is_published': ip_group[0].ip_is_published,
                    'ip_duplicity': ip_group[0].ip_duplicity,
                    'ip_duplicity_indexes': ip_group[0].ip_duplicity_indexes
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
            ip_groups_functions.create_transaction_log(
                action="GET",
                table="ip_groups",
                user_id=int(user_id),
                description=f"IP Group {ip_group_id} retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': f"IP Group {ip_group_id} retrieved successfully",
                'ip_group': request,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve IP Group {ip_group_id}: {str(e)}",
            'backend_status': 400
        }


@ip_groups_router.get("/blacklist/{site_id}")
async def get_blacklist_by_site(user_id: int, site_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_functions.verify_user_existence(user_id):
            group_metadata = {'site_id': site_id, 'group': 'blacklist'}
            request = ThreadingManager().run_thread(IPGroups.get_group_by_site, 'rx', group_metadata)
            ip_groups_functions.create_transaction_log(
                action="GET",
                table="ip_groups",
                user_id=int(user_id),
                description=f"Blacklist for Site {site_id} retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': f"Blacklist for Site {site_id} retrieved successfully",
                'length': len(request),
                'blacklist': request,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve Blacklist for Site {site_id}: {str(e)}",
            'backend_status': 400
        }


@ip_groups_router.get("/ip/authorized/{site_id}")
async def get_authorized_by_site(user_id: int, site_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_functions.verify_user_existence(user_id):
            group_metadata = {'site_id': site_id, 'group': 'authorized'}
            request = ThreadingManager().run_thread(IPGroups.get_group_by_site, 'rx', group_metadata)
            ip_groups_functions.create_transaction_log(
                action="GET",
                table="ip_groups",
                user_id=int(user_id),
                description=f"Authorized IPs for Site {site_id} retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': f"Authorized IPs for Site {site_id} retrieved successfully",
                'length': len(request),
                'authorized': request,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve Authorized IPs for Site {site_id}: {str(e)}",
            'backend_status': 400
        }


@ip_groups_router.get("/ip/availables/{site_id}")
async def get_available_by_site(user_id: int, site_id: int, metadata: Request):
    try:
        if ip_groups_functions.verify_user_existence(user_id):
            group_metadata = {'site_id': site_id}
            request = ThreadingManager().run_thread(IPGroups.get_available_authorized_by_site, 'rx', group_metadata)
            ip_groups_functions.create_transaction_log(
                action="GET",
                table="ip_groups",
                user_id=int(user_id),
                description=f"Available IPs for Site {site_id} retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': f"Available IPs for Site {site_id} retrieved successfully",
                'availables': request,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve Available IPs for Site {site_id}: {str(e)}",
            'backend_status': 400
        }


@ip_groups_router.put("/ip/group/{ip_group_id}")
async def update_ip_group(
        user_id: int,
        ip_group_id: int,
        ip_group_alias: str,
        ip_group_description: str,
        tags: IPGroupsTagsBase,
        metadata: Request,
        token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_functions.verify_user_existence(user_id):
            ip_group = IPGroupsEntity(
                ip_group_id=ip_group_id,
                ip_group_alias=ip_group_alias,
                ip_group_description=ip_group_description
            )
            ip_group_metadata = {'ip_group': ip_group, 'tags': tags.tags}
            ThreadingManager().run_thread(IPGroups.update_ip_group, 'rx', ip_group_metadata)
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


@ip_groups_router.put("/blacklist/move/to/authorized/{ip_group_id}")
async def move_blacklist_to_authorized(user_id: int, ip_group_id: int, metadata: Request,
                                       token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(IPGroups.move_from_blacklist_to_authorized, 'w', ip_group_id)
            ip_groups_functions.create_transaction_log(
                action="UPDATE",
                table="ip_groups",
                user_id=int(user_id),
                description=f"IP Group {ip_group_id} moved from Blacklist to Authorized",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': f"IP Group {ip_group_id} moved from Blacklist to Authorized",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to move IP Group {ip_group_id} from Blacklist to Authorized: {str(e)}",
            'backend_status': 400
        }


@ip_groups_router.put("/blacklist/move/to/authorized/bulk/")
async def move_blacklist_to_authorized_bulk(user_id: int, ip_groups_ids: BlacklistBulkMoveBase, metadata: Request,
                                            token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(IPGroups.bulk_move_from_blacklist_to_authorized, 'w', ip_groups_ids.ip_groups_ids)
            ip_groups_functions.create_transaction_log(
                action="UPDATE",
                table="ip_groups",
                user_id=int(user_id),
                description=f"IP Groups moved from Blacklist to Authorized",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': f"IP Groups moved from Blacklist to Authorized",
                'backend_status': 200,
                'count_flag': len(ip_groups_ids.ip_groups_ids)
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to move IP Groups from Blacklist to Authorized: {str(e)}",
            'backend_status': 400
        }


@ip_groups_router.put("/blacklist/move/all/to/authorized/{site_id}")
async def move_all_blacklist_to_authorized(user_id: int, site_id: int, metadata: Request,
                                           token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_functions.verify_user_existence(user_id):
            group_metadata = {'site_id': site_id, 'group': 'blacklist'}
            ThreadingManager().run_thread(IPGroups.move_all_from_blacklist_to_authorized, 'w', group_metadata)
            ip_groups_functions.create_transaction_log(
                action="UPDATE",
                table="ip_groups",
                user_id=int(user_id),
                description=f"All Blacklist IPs moved to Authorized for Site {site_id}",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': f"All Blacklist IPs moved to Authorized for Site {site_id}",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to move all Blacklist IPs to Authorized for Site {site_id}: {str(e)}",
            'backend_status': 400
        }


@ip_groups_router.delete("/ip/group/{ip_group_id}")
async def delete_ip_group(user_id: int, ip_group_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(IPGroups.delete_ip_group, 'w', ip_group_id)
            ip_groups_functions.create_transaction_log(
                action="DELETE",
                table="ip_groups",
                user_id=int(user_id),
                description=f"IP Group {ip_group_id} deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': f"IP Group {ip_group_id} deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete IP Group {ip_group_id}: {str(e)}",
            'backend_status': 400
        }


@ip_groups_router.delete("/ip/groups/bulk/")
async def delete_ip_groups_bulk(user_id: int, metadata: Request, request: IPGroupsBulkDeleteBase,
                                token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(IPGroups.bulk_delete_ip_groups, 'w', request.ip_groups_ids)
            ip_groups_functions.create_transaction_log(
                action="DELETE",
                table="ip_groups",
                user_id=int(user_id),
                description="IP Groups deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "IP Groups deleted successfully",
                'count_flag': len(request.ip_groups_ids),
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete IP Groups: {str(e)}",
            'backend_status': 400
        }


@ip_groups_router.delete("/ip/groups/")
async def delete_ip_groups(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(IPGroups.delete_ip_groups, 'wx')
            ip_groups_functions.create_transaction_log(
                action="DELETE",
                table="ip_groups",
                user_id=int(user_id),
                description="All IP Groups deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "All IP Groups deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete IP Groups: {str(e)}",
            'backend_status': 400
        }


@ip_groups_router.delete("/blacklist/site/{site_id}")
async def delete_blacklist_by_site(user_id: int, site_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_functions.verify_user_existence(user_id):
            group_metadata = {'site_id': site_id, 'group': 'blacklist'}
            ThreadingManager().run_thread(IPGroups.delete_ip_group_by_site, 'w', group_metadata)
            ip_groups_functions.create_transaction_log(
                action="DELETE",
                table="ip_groups",
                user_id=int(user_id),
                description=f"Blacklist for Site {site_id} deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': f"Blacklist for Site {site_id} deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete Blacklist for Site {site_id}: {str(e)}",
            'backend_status': 400
        }


@ip_groups_router.delete("/ip/authorized/site/{site_id}")
async def delete_authorized_by_site(user_id: int, site_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if ip_groups_functions.verify_user_existence(user_id):
            group_metadata = {'site_id': site_id, 'group': 'authorized'}
            ThreadingManager().run_thread(IPGroups.delete_ip_group_by_site, 'w', group_metadata)
            ip_groups_functions.create_transaction_log(
                action="DELETE",
                table="ip_groups",
                user_id=int(user_id),
                description=f"Authorized for Site {site_id} deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': f"Authorized for Site {site_id} deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete Authorized for Site {site_id}: {str(e)}",
            'backend_status': 400
        }
