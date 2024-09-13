from .metadata import app_metadata
from fastapi import FastAPI, APIRouter

from .routes.sites_api import sites_router
from .routes.regions_api import regions_router

fastapi_app = FastAPI(**app_metadata)

private_router = APIRouter(prefix='/private', tags=['Private API'])
private_router.include_router(sites_router, tags=['Sites'])
private_router.include_router(regions_router, tags=['Regions'])
fastapi_app.include_router(private_router, prefix='/api')
