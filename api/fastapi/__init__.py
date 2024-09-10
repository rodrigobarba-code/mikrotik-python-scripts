from fastapi import FastAPI
from .routes.regions_api import regions_router
fastapi_app = FastAPI()

fastapi_app.include_router(regions_router, prefix="/api")