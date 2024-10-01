from sqlalchemy import func, event
from sqlalchemy.orm import Session

from models.sites.models import Site
from models.routers.models import Router
from models.regions.models import Region
from models.users.models import User, UserLog
from models.router_scan.models import ARP, ARPTag
from models.ip_management.models import IPSegment