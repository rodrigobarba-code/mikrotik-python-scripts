from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

from entities.region import RegionEntity
from models.regions.models import Region
from utils.threading_manager import ThreadingManager

regions_router = APIRouter()

class RegionBulkDeleteBase(BaseModel):
    regions_ids: List[int]

@regions_router.get("/regions/")
async def get_regions():
    try:
        request = ThreadingManager().run_thread(Region.get_regions, 'r')
        region_list = [
            {"region_id": region.region_id, "region_name": region.region_name}
            for region in request
        ]
        return {
            'message': "Regions retrieved successfully",
            'regions': region_list,
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to retrieve regions: {str(e)}",
            'backend_status': 400
        }

@regions_router.get("/region/{region_id}")
async def get_region(region_id: int):
    try:
        request = ThreadingManager().run_thread(Region.get_region, 'rx', region_id)
        return {
            'message': "Region retrieved successfully",
            'region': {
                "region_id": request.region_id,
                "region_name": request.region_name
            },
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to retrieve region: {str(e)}",
            'backend_status': 400
        }

@regions_router.post("/region/")
async def add_region(region_name: str):
    try:
        region = RegionEntity(
            region_id=int(),
            region_name=region_name
        )
        ThreadingManager().run_thread(Region.add_region, 'w', region)
        return {
            'message': "Region added successfully",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to add region: {str(e)}",
            'backend_status': 400
        }

@regions_router.put("/region/{region_id}")
async def update_region(region_id: int, region_name: str):
    try:
        region = RegionEntity(
            region_id=region_id,
            region_name=region_name
        )
        ThreadingManager().run_thread(Region.update_region, 'w', region)
        return {
            'message': "Region updated successfully",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to update region: {str(e)}",
            'backend_status': 400
        }

@regions_router.delete("/region/{region_id}")
async def delete_region(region_id: int):
    try:
        ThreadingManager().run_thread(Region.delete_region, 'w', region_id)
        return {
            'message': "Region deleted successfully",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to delete region: {str(e)}",
            'backend_status': 400
        }

@regions_router.delete("/regions/bulk/")
async def bulk_delete_regions(request: RegionBulkDeleteBase):
    try:
        region_ids = request.regions_ids
        request = ThreadingManager().run_thread(Region.bulk_delete_regions, 'w', region_ids)
        return {
            'message': "Bulk delete regions successful",
            'count_flag': len(region_ids),
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to bulk delete regions: {str(e)}",
            'backend_status': 400
        }

@regions_router.delete("/regions/")
async def delete_all_regions():
    try:
        ThreadingManager().run_thread(Region.delete_all_regions, 'wx')
        return {
            'message': "All regions deleted successfully",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to delete all regions: {str(e)}",
            'backend_status': 400
        }
