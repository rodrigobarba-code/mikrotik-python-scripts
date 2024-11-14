from typing import List
from ...auth import verify_jwt
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request

from ...functions import APIFunctions
from entities.region import RegionEntity
from models.regions.models import Region
from utils.threading_manager import ThreadingManager

regions_router = APIRouter()
regions_functions = APIFunctions()

class RegionBulkDeleteBase(BaseModel):
    regions_ids: List[int]

class RegionBulkInsertBase(BaseModel):
    regions: List[dict]

@regions_router.get("/regions/")
async def get_regions(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if regions_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(Region.get_regions, 'r')
            region_list = [
                {"region_id": region.region_id, "region_name": region.region_name}
                for region in request
            ]
            regions_functions.create_transaction_log(
                action="GET",
                table="regions",
                user_id=int(user_id),
                description="Regions retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Regions retrieved successfully",
                'regions': region_list,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve regions: {str(e)}",
            'backend_status': 400
        }

@regions_router.get("/region/{region_id}")
async def get_region(user_id: int, metadata: Request, region_id: int, token: dict = Depends(verify_jwt)):
    try:
        if regions_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(Region.get_region, 'rx', region_id)
            region = {
                "region_id": request.region_id,
                "region_name": request.region_name
            }
            regions_functions.create_transaction_log(
                action="GET",
                table="regions",
                user_id=int(user_id),
                description="Region retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Region retrieved successfully",
                'region': region,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve region: {str(e)}",
            'backend_status': 400
        }

@regions_router.post("/region/")
async def add_region(user_id: int, metadata: Request, region_name: str, token: dict = Depends(verify_jwt)):
    try:
        if regions_functions.verify_user_existence(user_id):
            region = RegionEntity(
                region_id=int(),
                region_name=region_name
            )
            ThreadingManager().run_thread(Region.add_region, 'w', region)
            regions_functions.create_transaction_log(
                action="POST",
                table="regions",
                user_id=int(user_id),
                description="Region added successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Region added successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to add region: {str(e)}",
            'backend_status': 400
        }

@regions_router.put("/region/{region_id}")
async def update_region(user_id: int, metadata: Request, region_id: int, region_name: str, token: dict = Depends(verify_jwt)):
    try:
        if regions_functions.verify_user_existence(user_id):
            region = RegionEntity(
                region_id=region_id,
                region_name=region_name
            )
            ThreadingManager().run_thread(Region.update_region, 'w', region)
            regions_functions.create_transaction_log(
                action="PUT",
                table="regions",
                user_id=int(user_id),
                description="Region updated successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Region updated successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to update region: {str(e)}",
            'backend_status': 400
        }

@regions_router.delete("/region/{region_id}")
async def delete_region(user_id: str, metadata: Request, region_id: int, token: dict = Depends(verify_jwt)):
    try:
        if regions_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(Region.delete_region, 'w', region_id)
            ThreadingManager().run_thread(Region.verify_autoincrement_id, 'r')
            regions_functions.create_transaction_log(
                action="DELETE",
                table="regions",
                user_id=int(user_id),
                description="Region deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Region deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete region: {str(e)}",
            'backend_status': 400
        }

@regions_router.delete("/regions/bulk/")
async def bulk_delete_regions(user_id: str, metadata: Request, request: RegionBulkDeleteBase, token: dict = Depends(verify_jwt)):
    try:
        if regions_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(Region.bulk_delete_regions, 'w', request.regions_ids)
            ThreadingManager().run_thread(Region.verify_autoincrement_id, 'r')
            regions_functions.create_transaction_log(
                action="DELETE",
                table="regions",
                user_id=int(user_id),
                description="Regions deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Regions deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to bulk delete regions: {str(e)}",
            'backend_status': 400
        }

@regions_router.delete("/regions/")
async def delete_all_regions(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if regions_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(Region.delete_all_regions, 'wx')
            ThreadingManager().run_thread(Region.verify_autoincrement_id, 'r')
            regions_functions.create_transaction_log(
                action="DELETE",
                table="regions",
                user_id=int(user_id),
                description="All regions deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "All regions deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete all regions: {str(e)}",
            'backend_status': 400
        }

@regions_router.post("/bulk/insert/regions/")
async def bulk_insert_regions(
        user_id: int,
        metadata: Request,
        request: RegionBulkInsertBase,
        token: dict = Depends(verify_jwt)
):
    try:
        if regions_functions.verify_user_existence(user_id):
            regions = [
                RegionEntity(
                    region_id=int(),
                    region_name=region['region_name']
                )
                for region in request.regions
            ]
            ThreadingManager().run_thread(Region.bulk_insert_regions, 'w', regions)
            regions_functions.create_transaction_log(
                action="POST",
                table="regions",
                user_id=int(user_id),
                description="Regions bulk inserted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Regions bulk inserted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to bulk insert regions: {str(e)}",
            'backend_status': 400
        }
