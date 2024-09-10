from fastapi import APIRouter
from models.regions.models import Region
from entities.region import RegionEntity
from utils.threading_manager import ThreadingManager

regions_router = APIRouter()

@regions_router.get("/regions/")
async def get_regions():
    try:
        region_object = []
        regions = ThreadingManager().run_thread(Region.get_regions, 'r')
        for region in regions:
            region_object.append(
                {
                    "region_id": region.region_id,
                    "region_name": region.region_name
                }
            )
        return region_object
    except Exception as e:
        return {"message": str(e)}
    finally:
        pass

@regions_router.get("/regions/{region_id}")
async def get_region(region_id: int):
    try:
        region = ThreadingManager().run_thread(Region.get_region, 'rx', region_id)
        return {
            "region_id": region.region_id,
            "region_name": region.region_name
        }
    except Exception as e:
        return {"message": str(e)}
    finally:
        pass

@regions_router.post("/regions/")
async def create_region(region_name: str):
    try:
        region = RegionEntity(region_id=int(), region_name=region_name)
        ThreadingManager().run_thread(Region.add_region, 'w', region)
        return {"message": "Region added successfully"}
    except Exception as e:
        return {"message": str(e)}
    finally:
        pass

@regions_router.put("/regions/{region_id}")
async def update_region(region_id: int, region_name: str):
    try:
        region = RegionEntity(region_id=region_id, region_name=region_name)
        ThreadingManager().run_thread(Region.update_region, 'w', region)
        return {"message": "Region updated successfully"}
    except Exception as e:
        return {"message": str(e)}
    finally:
        pass

@regions_router.delete("/regions/{region_id}")
async def delete_region(region_id: int):
    try:
        ThreadingManager().run_thread(Region.delete_region, 'w', region_id)
        return {"message": "Region deleted successfully"}
    except Exception as e:
        return {"message": str(e)}
    finally:
        pass

@regions_router.delete("/regions/")
async def delete_all_regions():
    try:
        ThreadingManager().run_thread(Region.delete_all_regions, 'wx')
        return {"message": "All regions deleted successfully"}
    except Exception as e:
        return {"message": str(e)}
    finally:
        pass
