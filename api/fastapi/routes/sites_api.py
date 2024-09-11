from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

from entities.site import SiteEntity
from models.sites.models import Site
from utils.threading_manager import ThreadingManager

sites_router = APIRouter()

class SiteBulkDeleteBase(BaseModel):
    sites_ids: List[int]

@sites_router.get("/sites/")
async def get_sites():
    try:
        request = ThreadingManager().run_thread(Site.get_sites, 'r')
        site_list = [
            {
                "site_id": site.site_id,
                "fk_region_id": site.fk_region_id,
                "region_name": site.region_name,
                "site_name": site.site_name,
                "site_segment": site.site_segment
            }
            for site in request
        ]
        return {
            'message': "Sites retrieved successfully",
            'sites': site_list,
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to retrieve sites: {str(e)}",
            'backend_status': 400
        }

@sites_router.get("/site/{site_id}")
async def get_site(site_id: int):
    try:
        request = ThreadingManager().run_thread(Site.get_site, 'rx', site_id)
        return {
            'message': "Site retrieved successfully",
            'site': {
                "site_id": request.site_id,
                "fk_region_id": request.fk_region_id,
                "region_name": request.region_name,
                "site_name": request.site_name,
                "site_segment": request.site_segment
            },
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to retrieve site: {str(e)}",
            'backend_status': 400
        }

@sites_router.post("/site/")
async def add_site(fk_region_id: int, site_name: str, site_segment: int):
    try:
        site = SiteEntity(
            site_id=int(),
            fk_region_id=fk_region_id,
            site_name=site_name,
            region_name=str(),
            site_segment=site_segment
        )
        ThreadingManager().run_thread(Site.add_site, 'w', site)
        return {
            'message': "Site added successfully",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to add site: {str(e)}",
            'backend_status': 400
        }

@sites_router.put("/site/{site_id}")
async def update_site(site_id: int, fk_region_id: int, site_name: str, site_segment: int):
    try:
        site = SiteEntity(
            site_id=site_id,
            fk_region_id=fk_region_id,
            site_name=site_name,
            region_name=str(),
            site_segment=site_segment
        )
        ThreadingManager().run_thread(Site.update_site, 'w', site)
        return {
            'message': "Site updated successfully",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to update site: {str(e)}",
            'backend_status': 400
        }

@sites_router.delete("/site/{site_id}")
async def delete_site(site_id: int):
    try:
        ThreadingManager().run_thread(Site.delete_site, 'w', site_id)
        return {
            'message': "Site deleted successfully",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to delete site: {str(e)}",
            'backend_status': 400
        }

@sites_router.delete("/sites/bulk/")
async def bulk_delete_sites(request: SiteBulkDeleteBase):
    try:
        site_ids = request.sites_ids
        ThreadingManager().run_thread(Site.bulk_delete_sites, 'w', site_ids)
        return {
            'message': "Sites deleted successfully",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to delete sites: {str(e)}",
            'backend_status': 400
        }

@sites_router.delete("/sites/")
async def delete_all_sites():
    try:
        ThreadingManager().run_thread(Site.delete_sites, 'wx')
        return {
            'message': "Sites deleted successfully",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to delete sites: {str(e)}",
            'backend_status': 400
        }
