from typing import List
from ...auth import verify_jwt
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request

from ...functions import APIFunctions
from entities.router import RouterEntity
from models.routers.models import Router
from utils.threading_manager import ThreadingManager

routers_router = APIRouter()
routers_functions = APIFunctions()

class RouterBulkDeleteBase(BaseModel):
    routers_ids: List[int]

@routers_router.get("/routers/")
async def get_routers(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if routers_functions.verify_user_existence(user_id):
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
            routers_functions.create_transaction_log(
                action="GET",
                table="routers",
                user_id=int(user_id),
                description="Routers retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Routers retrieved successfully",
                'routers': router_list,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve routers: {str(e)}",
            'backend_status': 400
        }

@routers_router.get("/router/{router_id}")
async def get_router(user_id: int, metadata: Request, router_id: int, token: dict = Depends(verify_jwt)):
    try:
        if routers_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(Router.get_router, 'rx', router_id)
            router = {
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
            }
            routers_functions.create_transaction_log(
                action="GET",
                table="routers",
                user_id=int(user_id),
                description=f"Router with ID {router_id} retrieved successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': f"Router with ID {router_id} retrieved successfully",
                'router': router,
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to retrieve router: {str(e)}",
            'backend_status': 400
        }

@routers_router.get("/router/verify/{router_id}")
async def verify_router(user_id: int, metadata: Request, router_id: int, token: dict = Depends(verify_jwt)):
    from ...routeros.api import RouterAPI
    try:
        if routers_functions.verify_user_existence(user_id):
            request = ThreadingManager().run_thread(Router.get_router, 'rx', router_id)
            router = {
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
            }
            router_object = RouterAPI(
                router['router_ip'],
                router['router_username'],
                router['router_password']
            )
            router_object.set_api()
            is_connected = await RouterAPI.verify_router_connection(router_object.get_api())
            if is_connected:
                routers_functions.create_transaction_log(
                    action="GET",
                    table="routers",
                    user_id=int(user_id),
                    description=f"Router with ID {router_id} verified successfully",
                    public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
                )
                return {
                    'message': f"Router with ID {router_id} verified successfully",
                    'router': router,
                    'is_connected': 1,
                    'backend_status': 200
                }
            else:
                routers_functions.create_transaction_log(
                    action="GET",
                    table="routers",
                    user_id=int(user_id),
                    description=f"Router with ID {router_id} could not be verified",
                    public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
                )
                return {
                    'message': f"Router with ID {router_id} could not be verified",
                    'router': router,
                    'is_connected': 0,
                    'backend_status': 200
                }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to verify router with ID {router_id}: {str(e)}",
            'backend_status': 400
        }

@routers_router.get("/router/verify-credentials/")
async def verify_router_credentials(
        user_id: int,
        metadata: Request,
        router_ip: str,
        router_username: str,
        router_password: str,
        token: dict = Depends(verify_jwt)
    ):
    from ...routeros.api import RouterAPI
    try:
        if routers_functions.verify_user_existence(user_id):
            router = RouterAPI(router_ip, router_username, router_password)
            router.set_api()
            is_connected = await RouterAPI.verify_router_connection(router.get_api())
            if is_connected:
                routers_functions.create_transaction_log(
                    action="GET",
                    table="routers",
                    user_id=int(user_id),
                    description="Router credentials verified successfully",
                    public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
                )
                return {
                    'message': "Router credentials verified successfully",
                    'is_connected': 1,
                    'backend_status': 200
                }
            else:
                routers_functions.create_transaction_log(
                    action="GET",
                    table="routers",
                    user_id=int(user_id),
                    description="Router credentials could not be verified",
                    public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
                )
                return {
                    'message': "Router credentials could not be verified",
                    'is_connected': 0,
                    'backend_status': 200
                }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to verify router credentials: {str(e)}",
            'backend_status': 400
        }

@routers_router.get("/router/verify/all/")
async def verify_all_routers(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    from ...routeros.api import RouterAPI
    try:
        if routers_functions.verify_user_existence(user_id):
            routers = ThreadingManager().run_thread(Router.get_routers, 'r')
            for router in routers:
                router_object = RouterAPI(
                    router.router_ip,
                    router.router_username,
                    router.router_password
                )
                router_object.set_api()
                is_connected = await RouterAPI.verify_router_connection(router_object.get_api())
                if is_connected:
                    routers_functions.create_transaction_log(
                        action="GET",
                        table="routers",
                        user_id=int(user_id),
                        description="All routers verified successfully",
                        public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
                    )
                    return {
                        'message': "All routers verified successfully",
                        'is_connected': 1,
                        'backend_status': 200
                    }
                else:
                    routers_functions.create_transaction_log(
                        action="GET",
                        table="routers",
                        user_id=int(user_id),
                        description="All routers could not be verified",
                        public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
                    )
                    return {
                        'message': "All routers could not be verified",
                        'is_connected': 0,
                        'backend_status': 200
                    }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to verify routers: {str(e)}",
            'backend_status': 400
        }

@routers_router.get("/routers/allow-scan/")
async def allow_scan_all_routers(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if routers_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(Router.allow_scan_all, 'wx')
            routers_functions.create_transaction_log(
                action="GET",
                table="routers",
                user_id=int(user_id),
                description="All routers are allowed to scan",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "All routers are allowed to scan",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to allow scan on routers: {str(e)}",
            'backend_status': 400
        }

@routers_router.get("/routers/deny-scan/")
async def deny_scan_all_routers(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if routers_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(Router.deny_scan_all, 'wx')
            routers_functions.create_transaction_log(
                action="GET",
                table="routers",
                user_id=int(user_id),
                description="All routers are denied to scan",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "All routers are denied to scan",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to deny scan on routers: {str(e)}",
            'backend_status': 400
        }

@routers_router.post("/router/")
async def add_router(
        user_id: int,
        metadata: Request,
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
        if routers_functions.verify_user_existence(user_id):
            router = RouterEntity(
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
            routers_functions.create_transaction_log(
                action="POST",
                table="routers",
                user_id=int(user_id),
                description="Router added successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Router added successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to add router: {str(e)}",
            'backend_status': 400
        }

@routers_router.put("/router/{router_id}")
async def update_router(
        user_id: int,
        metadata: Request,
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
        if routers_functions.verify_user_existence(user_id):
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
            routers_functions.create_transaction_log(
                action="PUT",
                table="routers",
                user_id=int(user_id),
                description="Router updated successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Router updated successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to update router: {str(e)}",
            'backend_status': 400
        }

@routers_router.delete("/router/{router_id}")
async def delete_router(user_id: int, metadata: Request, router_id: int, token: dict = Depends(verify_jwt)):
    try:
        if routers_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(Router.delete_router, 'w', router_id)
            routers_functions.create_transaction_log(
                action="DELETE",
                table="routers",
                user_id=int(user_id),
                description=f"Router with ID {router_id} deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': f"Router with ID {router_id} deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete router: {str(e)}",
            'backend_status': 400
        }

@routers_router.delete("/routers/bulk/")
async def bulk_delete_routers(user_id: int, metadata: Request, request: RouterBulkDeleteBase, token: dict = Depends(verify_jwt)):
    try:
        if routers_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(Router.bulk_delete_routers, 'w', request.routers_ids)
            routers_functions.create_transaction_log(
                action="DELETE",
                table="routers",
                user_id=int(user_id),
                description="Routers deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "Routers deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete routers: {str(e)}",
            'backend_status': 400
        }

@routers_router.delete("/routers/")
async def delete_all_routers(user_id: int, metadata: Request, token: dict = Depends(verify_jwt)):
    try:
        if routers_functions.verify_user_existence(user_id):
            ThreadingManager().run_thread(Router.delete_all_routers, 'wx')
            routers_functions.create_transaction_log(
                action="DELETE",
                table="routers",
                user_id=int(user_id),
                description="All routers deleted successfully",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': "All routers deleted successfully",
                'backend_status': 200
            }
        else:
            raise Exception("User not registered in the system")
    except Exception as e:
        return {
            'message': f"Failed to delete routers: {str(e)}",
            'backend_status': 400
        }
