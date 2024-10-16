from typing import List
from ...auth import verify_jwt
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request

from ...functions import APIFunctions
from entities.router import RouterEntity
from models.routers.models import Router
from utils.threading_manager import ThreadingManager

blacklist_router = APIRouter()
blacklist_functions = APIFunctions()
