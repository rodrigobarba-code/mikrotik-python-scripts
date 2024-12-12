from typing import List
from ...auth import verify_jwt
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request

from entities.site import SiteEntity
from models.sites.models import Site
from ...functions import APIFunctions
from utils.threading_manager import ThreadingManager

sites_router = APIRouter()
sites_functions = APIFunctions()


class SiteBulkDeleteBase(BaseModel):
    sites_ids: List[int]


class SiteBulkInsertBase(BaseModel):
    sites: List[dict]


@sites_router.get("/sites/")
async def get_sites(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if sites_functions.verify_user_existence(user_id):
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
            sites_functions.create_transaction_log(
                action="GET",
                table="sites",
                user_id=int(user_id),
                description="Sites retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Sites retrieved successfully",
                'sites': site_list,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve sites: {str(e)}",
            'backend_status': 400
        }


@sites_router.get("/site/{site_id}")
async def get_site(user_id: int, metadata: Request, site_id: int, token: dict = Depends(verify_jwt)):
    try:
        if sites_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(Site.get_site, 'rx', site_id)
            site = {
                "site_id": request.site_id,
                "fk_region_id": request.fk_region_id,
                "region_name": request.region_name,
                "site_name": request.site_name,
                "site_segment": request.site_segment
            }
            sites_functions.create_transaction_log(
                action="GET",
                table="sites",
                user_id=int(user_id),
                description="Site retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Site retrieved successfully",
                'site': site,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve site: {str(e)}",
            'backend_status': 400
        }


@sites_router.get("/sites/available/")
async def get_available_sites(
        user_id: int,
        metadata: Request,
        token: dict = Depends(verify_jwt)
):
    try:
        if sites_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(Site.get_available_sites, 'r')
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
            sites_functions.create_transaction_log(
                action="GET",
                table="sites",
                user_id=int(user_id),
                description="Available sites retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Available sites retrieved successfully",
                'sites': site_list,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve available sites: {str(e)}",
            'backend_status': 400
        }


@sites_router.post("/site/")
async def add_site(user_id: int, metadata: Request, fk_region_id: int, site_name: str, site_segment: int,
                   token: dict = Depends(verify_jwt)):
    try:
        if sites_functions.verify_user_existence(user_id):
            site = SiteEntity(
                site_id=int(),
                fk_region_id=fk_region_id,
                site_name=site_name,
                region_name=str(),
                site_segment=site_segment
            )
            ThreadingManager().run_thread(Site.add_site, 'w', site)
            sites_functions.create_transaction_log(
                action="POST",
                table="sites",
                user_id=int(user_id),
                description="Site added successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Site added successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to add site: {str(e)}",
            'backend_status': 400
        }


@sites_router.put("/site/{site_id}")
async def update_site(user_id: int, metadata: Request, site_id: int, fk_region_id: int, site_name: str,
                      site_segment: int, token: dict = Depends(verify_jwt)):
    try:
        if sites_functions.verify_user_existence(user_id):
            site = SiteEntity(
                site_id=site_id,
                fk_region_id=fk_region_id,
                site_name=site_name,
                region_name=str(),
                site_segment=site_segment
            )
            ThreadingManager().run_thread(Site.update_site, 'w', site)
            sites_functions.create_transaction_log(
                action="PUT",
                table="sites",
                user_id=int(user_id),
                description="Site updated successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Site updated successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to update site: {str(e)}",
            'backend_status': 400
        }


@sites_router.delete("/site/{site_id}")
async def delete_site(user_id: int, metadata: Request, site_id: int, token: dict = Depends(verify_jwt)):
    try:
        if sites_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(Site.delete_site, 'w', site_id)
            ThreadingManager().run_thread(Site.verify_autoincrement_id, 'r')
            sites_functions.create_transaction_log(
                action="DELETE",
                table="sites",
                user_id=int(user_id),
                description="Site deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Site deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete site: {str(e)}",
            'backend_status': 400
        }


@sites_router.delete("/sites/bulk/")
async def bulk_delete_sites(user_id: int, metadata: Request, request: SiteBulkDeleteBase,
                            token: dict = Depends(verify_jwt)):
    try:
        if sites_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(Site.bulk_delete_sites, 'w', request.sites_ids)
            ThreadingManager().run_thread(Site.verify_autoincrement_id, 'r')
            sites_functions.create_transaction_log(
                action="DELETE",
                table="sites",
                user_id=int(user_id),
                description="Sites deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Sites deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete sites: {str(e)}",
            'backend_status': 400
        }


@sites_router.delete("/sites/")
async def delete_all_sites(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if sites_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(Site.delete_sites, 'wx')
            ThreadingManager().run_thread(Site.verify_autoincrement_id, 'r')
            sites_functions.create_transaction_log(
                action="DELETE",
                table="sites",
                user_id=int(user_id),
                description="Sites deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Sites deleted successfully",
                'backend_status': 200
            }
    except Exception as e:
        return {
            'message': f"Failed to delete sites: {str(e)}",
            'backend_status': 400
        }


@sites_router.post("/bulk/insert/sites/")
async def bulk_insert_sites(
        user_id: int,
        metadata: Request,
        request: SiteBulkInsertBase,
        token: dict = Depends(verify_jwt)
):
    try:
        if sites_functions.verify_user_existence(user_id):
            sites = [
                SiteEntity(
                    site_id=int(),
                    fk_region_id=site['fk_region_id'],
                    site_name=site['site_name'],
                    region_name=str(),
                    site_segment=site['site_segment']
                )
                for site in request.sites
            ]
            ThreadingManager().run_thread(Site.bulk_insert_sites, 'w', sites)
            sites_functions.create_transaction_log(
                action="POST",
                table="sites",
                user_id=int(user_id),
                description="Sites bulk inserted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Sites bulk inserted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to bulk insert sites: {str(e)}",
            'backend_status': 400
        }


# resource for obtain the site name with ipsegments
@sites_router.get("/sites/with-ip-segment/")
async def get_site_with_ip_segment(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if sites_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(Site.get_sites_with_segments, 'r')
            site_list = [
                {
                    "site_id": site.site_id,
                    "site_name": site.site_name
                }
                for site in request
            ]
            sites_functions.create_transaction_log(
                action="GET",
                table="sites",
                user_id=int(user_id),
                description="Sites retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Sites retrieved successfully",
                'sites': site_list,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve sites: {str(e)}",
            'backend_status': 400
        }
