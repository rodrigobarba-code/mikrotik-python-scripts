from typing import List
from ...auth import verify_jwt
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request
from utils.threading_manager import ThreadingManager

from ...functions import APIFunctions
from models.ip_management.models import IPSegment

segments_router = APIRouter()
segments_functions = APIFunctions()

class SegmentBulkDeleteBase(BaseModel):
    segments_ids: List[int]

@segments_router.get("/segments/")
async def get_segments(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if segments_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(IPSegment.get_ip_segments, 'r')
            segments = [
                {
                    "ip_segment_id": segment.ip_segment_id,
                    "fk_router_id": segment.fk_router_id,
                    "ip_segment_ip": segment.ip_segment_ip,
                    "ip_segment_mask": segment.ip_segment_mask,
                    "ip_segment_network": segment.ip_segment_network,
                    "ip_segment_interface": segment.ip_segment_interface,
                    "ip_segment_actual_iface": segment.ip_segment_actual_iface,
                    "ip_segment_tag": segment.ip_segment_tag,
                    "ip_segment_comment": segment.ip_segment_comment,
                    "ip_segment_is_invalid": segment.ip_segment_is_invalid,
                    "ip_segment_is_dynamic": segment.ip_segment_is_dynamic,
                    "ip_segment_is_disabled": segment.ip_segment_is_disabled
                }
                for segment in request
            ]
            segments_functions.create_transaction_log(
                action="GET",
                table="segments",
                user_id=int(user_id),
                description="Segments table retrieved",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Segments table retrieved successfully",
                'segments': segments,
                'lenght': len(segments),
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve Segments table: {str(e)}",
            'backend_status': 400
        }

@segments_router.get("/segment/{segment_id}")
async def get_segment(user_id: int, metadata: Request, segment_id: int, token: dict = Depends(verify_jwt)):
    try:
        if segments_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(IPSegment.get_ip_segment, 'rx', segment_id)
            segment = {
                "ip_segment_id": request.ip_segment_id,
                "fk_router_id": request.fk_router_id,
                "ip_segment_ip": request.ip_segment_ip,
                "ip_segment_mask": request.ip_segment_mask,
                "ip_segment_network": request.ip_segment_network,
                "ip_segment_interface": request.ip_segment_interface,
                "ip_segment_actual_iface": request.ip_segment_actual_iface,
                "ip_segment_tag": request.ip_segment_tag,
                "ip_segment_comment": request.ip_segment_comment,
                "ip_segment_is_invalid": request.ip_segment_is_invalid,
                "ip_segment_is_dynamic": request.ip_segment_is_dynamic,
                "ip_segment_is_disabled": request.ip_segment_is_disabled
            }
            segments_functions.create_transaction_log(
                action="GET",
                table="segments",
                user_id=int(user_id),
                description=f"Segment {segment_id} retrieved",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': f"Segment {segment_id} retrieved successfully",
                'segment': segment,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve Segment {segment_id}: {str(e)}",
            'backend_status': 400
        }

@segments_router.get("/segment/site/{site_id}")
async def get_segments_by_site(user_id: int, metadata: Request, site_id: int, token: dict = Depends(verify_jwt)):
    try:
        if segments_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(IPSegment.get_ip_segments_by_site_id, 'rx', site_id)
            segments = [
                {
                    "ip_segment_id": segment.ip_segment_id,
                    "fk_router_id": segment.fk_router_id,
                    "ip_segment_ip": segment.ip_segment_ip,
                    "ip_segment_mask": segment.ip_segment_mask,
                    "ip_segment_network": segment.ip_segment_network,
                    "ip_segment_interface": segment.ip_segment_interface,
                    "ip_segment_actual_iface": segment.ip_segment_actual_iface,
                    "ip_segment_tag": segment.ip_segment_tag,
                    "ip_segment_comment": segment.ip_segment_comment,
                    "ip_segment_is_invalid": segment.ip_segment_is_invalid,
                    "ip_segment_is_dynamic": segment.ip_segment_is_dynamic,
                    "ip_segment_is_disabled": segment.ip_segment_is_disabled
                }
                for segment in request
            ]
            segments_functions.create_transaction_log(
                action="GET",
                table="segments",
                user_id=int(user_id),
                description=f"Segments for Site {site_id} retrieved",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': f"Segments for Site {site_id} retrieved successfully",
                'segments': segments,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve Segments for Site {site_id}: {str(e)}",
            'backend_status': 400
        }

@segments_router.get("/segment/router/{router_id}")
async def get_segments_by_router(user_id: int, metadata: Request, router_id: int, token: dict = Depends(verify_jwt)):
    try:
        if segments_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(IPSegment.get_ip_segments_by_router_id, 'rx', router_id)
            segments = [
                {
                    "ip_segment_id": segment.ip_segment_id,
                    "fk_router_id": segment.fk_router_id,
                    "ip_segment_ip": segment.ip_segment_ip,
                    "ip_segment_mask": segment.ip_segment_mask,
                    "ip_segment_network": segment.ip_segment_network,
                    "ip_segment_interface": segment.ip_segment_interface,
                    "ip_segment_actual_iface": segment.ip_segment_actual_iface,
                    "ip_segment_tag": segment.ip_segment_tag,
                    "ip_segment_comment": segment.ip_segment_comment,
                    "ip_segment_is_invalid": segment.ip_segment_is_invalid,
                    "ip_segment_is_dynamic": segment.ip_segment_is_dynamic,
                    "ip_segment_is_disabled": segment.ip_segment_is_disabled
                }
                for segment in request
            ]
            segments_functions.create_transaction_log(
                action="GET",
                table="segments",
                user_id=int(user_id),
                description=f"Segments for Router {router_id} retrieved",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': f"Segments for Router {router_id} retrieved successfully",
                'segments': segments,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve Segments for Router {router_id}: {str(e)}",
            'backend_status': 400
        }

@segments_router.delete("/segments/site/{site_id}")
async def delete_segments(user_id: int, metadata: Request, site_id:int, token: dict = Depends(verify_jwt)):
    try:
        if segments_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(IPSegment.delete_ip_segments_by_site, 'w', site_id)
            ThreadingManager().run_thread(IPSegment.verify_autoincrement_id, 'r')
            segments_functions.create_transaction_log(
                action="DELETE",
                table="segments",
                user_id=int(user_id),
                description="Segments table deleted",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Segments table deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete Segments table: {str(e)}",
            'backend_status': 400
        }

@segments_router.delete("/segments/")
async def delete_segments(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if segments_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(IPSegment.delete_ip_segments, 'wx')
            ThreadingManager().run_thread(IPSegment.verify_autoincrement_id, 'r')
            segments_functions.create_transaction_log(
                action="DELETE",
                table="segments",
                user_id=int(user_id),
                description="Segments table deleted",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Segments table deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete Segments table: {str(e)}",
            'backend_status': 400
        }

@segments_router.delete("/segment/{segment_id}")
async def delete_segment(user_id: int, metadata: Request, segment_id: int, token: dict = Depends(verify_jwt)):
    try:
        if segments_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(IPSegment.delete_ip_segment, 'rxc', segment_id)
            ThreadingManager().run_thread(IPSegment.verify_autoincrement_id, 'r')
            segments_functions.create_transaction_log(
                action="DELETE",
                table="segments",
                user_id=int(user_id),
                description=f"Segment {segment_id} deleted",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': f"Segment {segment_id} deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete Segment {segment_id}: {str(e)}",
            'backend_status': 400
        }

@segments_router.delete("/segments/bulk/")
async def bulk_delete_segments(user_id: int, metadata: Request, request: SegmentBulkDeleteBase, token: dict = Depends(verify_jwt)):
    try:
        if segments_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(IPSegment.bulk_delete_ip_segments, 'w', request.segments_ids)
            ThreadingManager().run_thread(IPSegment.verify_autoincrement_id, 'r')
            segments_functions.create_transaction_log(
                action="DELETE",
                table="segments",
                user_id=int(user_id),
                description="Segments table deleted",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Segments table deleted successfully",
                'backend_status': 200,
                'count_flag': len(request.segments_ids)
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete Segments table: {str(e)}",
            'backend_status': 400
        }
