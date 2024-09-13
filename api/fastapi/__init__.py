from .metadata import app_metadata
from fastapi import FastAPI, APIRouter

from .routes.sites_api import sites_router
from .routes.regions_api import regions_router
from .routes.routers_api import routers_router

fastapi_app = FastAPI(**app_metadata)

private_router = APIRouter(prefix='/private', tags=['Private API'])
private_router.include_router(sites_router, tags=['Sites'])
private_router.include_router(regions_router, tags=['Regions'])
private_router.include_router(routers_router, tags=['Routers'])
fastapi_app.include_router(private_router, prefix='/api')
