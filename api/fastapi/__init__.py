from .metadata import app_metadata
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from .routes.logs_api import logs_router
from .routes.users_api import users_router
from .routes.sites_api import sites_router
from .routes.regions_api import regions_router
from .routes.routers_api import routers_router

fastapi_app = FastAPI(**app_metadata)

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

private_router = APIRouter(prefix='/private')
private_router.include_router(logs_router, tags=['Logs'])
private_router.include_router(users_router, tags=['Users'])
private_router.include_router(sites_router, tags=['Sites'])
private_router.include_router(regions_router, tags=['Regions'])
private_router.include_router(routers_router, tags=['Routers'])
fastapi_app.include_router(private_router, prefix='/api')
