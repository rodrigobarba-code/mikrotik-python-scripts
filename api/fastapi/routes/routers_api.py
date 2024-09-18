from typing import List
from ..auth import verify_jwt
from pydantic import BaseModel
from fastapi import APIRouter, Depends

from entities.router import RouterEntity
from models.routers.models import Router
from utils.threading_manager import ThreadingManager

routers_router = APIRouter()

class RouterBulkDeleteBase(BaseModel):
    routers_ids: List[int]

@routers_router.get("/routers/")
async def get_routers(token: dict = Depends(verify_jwt)):
    try:
        request = ThreadingManager().run_thread(Router.get_routers, 'r')
        router_list = [
            {
                "router_id": router.router_id,
                "router_name": router.router_name,
                "router_description": router.router_description,
                "router_brand": router.router_brand,
                "router_model": router.router_model,
                "fk_site_id": router.fk_site_id,
                "router_ip": router.router_ip,
                "router_mac": router.router_mac,
                "router_username": router.router_username,
                "router_password": router.router_password,
                "allow_scan": router.allow_scan
            }
            for router in request
        ]
        return {
            'message': "Routers retrieved successfully",
            'routers': router_list,
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to retrieve routers: {str(e)}",
            'backend_status': 400
        }

@routers_router.get("/router/{router_id}")
async def get_router(router_id: int, token: dict = Depends(verify_jwt)):
    try:
        request = ThreadingManager().run_thread(Router.get_router, 'rx', router_id)
        return {
            'message': "Router retrieved successfully",
            'router': {
                "router_id": request.router_id,
                "router_name": request.router_name,
                "router_description": request.router_description,
                "router_brand": request.router_brand,
                "router_model": request.router_model,
                "fk_site_id": request.fk_site_id,
                "router_ip": request.router_ip,
                "router_mac": request.router_mac,
                "router_username": request.router_username,
                "router_password": request.router_password,
                "allow_scan": request.allow_scan
            },
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to retrieve router: {str(e)}",
            'backend_status': 400
        }

@routers_router.get("/router/verify/{router_id}")
async def verify_router(router_id: int, token: dict = Depends(verify_jwt)):
    from ...routeros.api import RouterAPI
    try:
        request = ThreadingManager().run_thread(Router.get_router, 'rx', router_id)
        router = RouterAPI(
            request.router_ip,
            request.router_username,
            request.router_password
        )
        router.set_api()
        is_connected = await RouterAPI.verify_router_connection(router.get_api())
        if is_connected:
            return {
                'message': f"Router with name {request.router_name} verified successfully",
                'is_connected': 1,
                'backend_status': 200
            }
        else:
            return {
                'message': f"Router with name {request.router_name} could not be verified",
                'is_connected': 0,
                'backend_status': 200
            }
    except Exception as e:
        return {
            'message': f"Failed to verify router with ID {router_id}: {str(e)}",
            'backend_status': 400
        }

@routers_router.get("/router/verify-credentials/")
async def verify_router_credentials(
        router_ip: str,
        router_username: str,
        router_password: str,
        token: dict = Depends(verify_jwt)
    ):
    from ...routeros.api import RouterAPI
    try:
        router = RouterAPI(
            router_ip,
            router_username,
            router_password
        )
        router.set_api()
        is_connected = await RouterAPI.verify_router_connection(router.get_api())
        if is_connected:
            return {
                'message': "Router credentials verified successfully",
                'is_connected': 1,
                'backend_status': 200
            }
        else:
            return {
                'message': "Router credentials could not be verified",
                'is_connected': 0,
                'backend_status': 200
            }
    except Exception as e:
        return {
            'message': f"Failed to verify router credentials: {str(e)}",
            'backend_status': 400
        }

@routers_router.get("/router/verify/all/")
async def verify_all_routers(token: dict = Depends(verify_jwt)):
    from ...routeros.api import RouterAPI
    try:
        flag_error = False
        request = ThreadingManager().run_thread(Router.get_routers, 'r')
        routers = [
            {
                "router_id": router.router_id,
                "router_object": RouterAPI(
                    router.router_ip,
                    router.router_username,
                    router.router_password
                )
            }
            for router in request
        ]
        for router in routers:
            router['router_object'].set_api()
            flag = await RouterAPI.verify_router_connection(router['router_object'].get_api())
            if not flag:
                router_id = router['router_id']
                flag_error = True
                break

        if not flag_error:
            return {
                'message': "All routers established connection successfully",
                'is_connected': 1,
                'backend_status': 200
            }
        else:
            return {
                'message': "A router could not be verified, check the logs",
                'is_connected': 0,
                'router_id': router_id,
                'backend_status': 200
            }
    except Exception as e:
        return {
            'message': f"Failed to verify routers: {str(e)}",
            'backend_status': 400
        }

@routers_router.get("/routers/allow-scan/")
async def allow_scan_all_routers(token: dict = Depends(verify_jwt)):
    try:
        ThreadingManager().run_thread(Router.allow_scan_all, 'wx')
        return {
            'message': "All routers are allowed to scan",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to allow scan on routers: {str(e)}",
            'backend_status': 400
        }

@routers_router.get("/routers/deny-scan/")
async def deny_scan_all_routers(token: dict = Depends(verify_jwt)):
    try:
        ThreadingManager().run_thread(Router.deny_scan_all, 'wx')
        return {
            'message': "All routers are denied to scan",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to deny scan on routers: {str(e)}",
            'backend_status': 400
        }

@routers_router.post("/router/")
async def add_router(
        router_name: str,
        router_description: str,
        router_brand: str,
        router_model: str,
        fk_site_id: int,
        router_ip: str,
        router_mac: str,
        router_username: str,
        router_password: str,
        allow_scan: int,
        token: dict = Depends(verify_jwt)
    ):
    try:
        router = RouterEntity(
            router_id=int(),
            router_name=router_name,
            router_description=router_description,
            router_brand=router_brand,
            router_model=router_model,
            fk_site_id=fk_site_id,
            router_ip=router_ip,
            router_mac=router_mac,
            router_username=router_username,
            router_password=router_password,
            allow_scan=allow_scan
        )
        ThreadingManager().run_thread(Router.add_router, 'w', router)
        return {
            'message': "Router added successfully",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to add router: {str(e)}",
            'backend_status': 400
        }

@routers_router.put("/router/{router_id}")
async def update_router(
        router_id: int,
        router_name: str,
        router_description: str,
        router_brand: str,
        router_model: str,
        fk_site_id: int,
        router_ip: str,
        router_mac: str,
        router_username: str,
        router_password: str,
        allow_scan: int,
        token: dict = Depends(verify_jwt)
    ):
    try:
        router = RouterEntity(
            router_id=router_id,
            router_name=router_name,
            router_description=router_description,
            router_brand=router_brand,
            router_model=router_model,
            fk_site_id=fk_site_id,
            router_ip=router_ip,
            router_mac=router_mac,
            router_username=router_username,
            router_password=router_password,
            allow_scan=allow_scan
        )
        ThreadingManager().run_thread(Router.update_router, 'w', router)
        return {
            'message': "Router updated successfully",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to update router: {str(e)}",
            'backend_status': 400
        }

@routers_router.delete("/router/{router_id}")
async def delete_router(router_id: int, token: dict = Depends(verify_jwt)):
    try:
        ThreadingManager().run_thread(Router.delete_router, 'w', router_id)
        return {
            'message': "Router deleted successfully",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to delete router: {str(e)}",
            'backend_status': 400
        }

@routers_router.delete("/routers/bulk/")
async def bulk_delete_routers(request: RouterBulkDeleteBase, token: dict = Depends(verify_jwt)):
    try:
        router_ids = request.routers_ids
        ThreadingManager().run_thread(Router.bulk_delete_routers, 'w', router_ids)
        return {
            'message': "Routers deleted successfully",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to delete routers: {str(e)}",
            'backend_status': 400
        }

@routers_router.delete("/routers/")
async def delete_all_routers(token: dict = Depends(verify_jwt)):
    try:
        ThreadingManager().run_thread(Router.delete_routers, 'wx')
        return {
            'message': "Routers deleted successfully",
            'backend_status': 200
        }
    except Exception as e:
        return {
            'message': f"Failed to delete routers: {str(e)}",
            'backend_status': 400
        }
