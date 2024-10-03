from .config import DatabaseConfig
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, event, create_engine
from sqlalchemy.ext.declarative import declarative_base

def init_models():
    from models.sites.models import Site
    from models.regions.models import Region
    from models.routers.models import Router
    from models.router_scan.models import ARP
    from models.router_scan.models import ARPTags
    from models.users.models import User, UserLog
    from models.ip_management.models import IPSegment

Base = declarative_base()
engine = create_engine(
    DatabaseConfig.SQLALCHEMY_DATABASE_URI,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
