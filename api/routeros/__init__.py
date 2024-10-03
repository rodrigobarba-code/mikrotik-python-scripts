from fastapi import APIRouter

from .routes.scan_api import scan_router

routeros_router = APIRouter(prefix='/private', tags=['RouterOS'])

routeros_router.include_router(scan_router, tags=['Scan API'])
