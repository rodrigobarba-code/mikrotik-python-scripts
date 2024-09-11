from fastapi import FastAPI

from .routes.sites_api import sites_router
from .routes.regions_api import regions_router

fastapi_app = FastAPI(
    title='Seven Suite Application FastAPI Backend',
    description='## FastAPI Backend for Seven Suite Application',
    version='0.0.1-alpha',
    terms_of_service='http://localhost:8080/terms/',
    contact={
        'name': 'Seven Suite',
        'url': 'http://localhost:8080/contact/',
        'email': 'luisrodrigobarba.work@outlook.com'
    },
    license_info={
        'name': 'Apache 2.0',
        'url': 'https://www.apache.org/licenses/LICENSE-2.0.html'
    }
)

(
    fastapi_app.include_router(sites_router, prefix='/api', tags=['Sites']),
    fastapi_app.include_router(regions_router, prefix='/api', tags=['Regions'])
)
