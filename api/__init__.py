from fastapi import FastAPI
from api.metadata import app_metadata as metadata
from fastapi.middleware.cors import CORSMiddleware

from .fastapi import private_router
fastapi_app = FastAPI(**metadata)

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

fastapi_app.include_router(private_router, prefix='/api')
# fastapi_app.include_router(public_router, prefix='/public')
