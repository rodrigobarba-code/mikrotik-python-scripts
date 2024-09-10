from .. import Base
from sqlalchemy import func
from sqlalchemy import Column, Integer, String

from models.sites.models import Site
from models.regions.exceptions import *
from entities.region import RegionEntity

class Region(Base):
    __tablename__ = 'regions'  

    region_id = Column(Integer, primary_key=True, autoincrement=True)  
    region_name = Column(String(128), nullable=False)  

    def __repr__(self):
        return f'<Region {self.region_id}>'  

    def to_dict(self):
        return {
            'region_id': self.region_id,  
            'region_name': self.region_name  
        }

    @staticmethod
    def add_region(session, region):
        try:
            if session.query(Region).filter(func.lower(Region.region_name) == func.lower(region.region_name)).first():
                raise RegionAlreadyExists(
                    region_id=session.query(Region).filter(func.lower(Region.region_name) == func.lower(region.region_name)).first().region_id,
                    region_name=region.region_name  
                )
            else:
                new_region = Region(
                    region_name=region.region_name  
                )
                region.validate()  
                session.add(new_region)
        except RegionAlreadyExists as e:
            raise e  
        except Exception as e:
            raise RegionError()

    @staticmethod
    def update_region(session, new_region):
        try:
            if not session.query(Region).get(new_region.region_id):
                raise RegionNotFound(
                    new_region.region_id  
                )
            else:
                old_region = session.query(Region).get(new_region.region_id)
                if old_region.region_name != new_region.region_name:
                    if session.query(Region).filter(func.lower(Region.region_name) == func.lower(new_region.region_name)).first():
                        raise RegionAlreadyExists(
                            region_id=session.query(Region).filter(func.lower(Region.region_name) == func.lower(new_region.region_name)).first().region_id,
                            region_name=new_region.region_name
                        )
                    else:
                        old_region.region_name = new_region.region_name
                        session.add(old_region)
        except RegionAlreadyExists as e:
            raise e  
        except RegionNotFound as e:
            raise e  
        except Exception as e:
            raise RegionError()

    @staticmethod
    def delete_region(session, region_id):
        try:
            if not session.query(Region).get(region_id):
                raise RegionNotFound(region_id)
            else:
                if session.query(Site).filter(Site.fk_region_id == region_id).first():
                    raise RegionAssociatedWithSite(
                        region_id=region_id,  
                        site_id=session.query(Site).filter(Site.fk_region_id == region_id).first().site_id  
                    )
                else:
                    region = session.query(Region).get(region_id)
                    session.delete(region)
        except RegionAssociatedWithSite as e:
            raise e  
        except RegionNotFound as e:
            raise e  
        except Exception as e:
            raise RegionError()

    @staticmethod
    def delete_all_regions(session):
        try:
            session.query(Region).delete()
            session.commit()  
        except Exception as e:
            raise RegionError()
    
    @staticmethod
    def get_region(session, region_id):
        try:
            if not session.query(Region).get(region_id):
                raise RegionNotFound(region_id)
            else:
                tmp = session.query(Region).get(region_id).to_dict()
                region = RegionEntity(
                    tmp['region_id'],  
                    tmp['region_name']  
                )
                region.validate()  
                return region
        except RegionNotFound as e:  
            raise e  
        except Exception as e:  
            raise RegionError()
    
    @staticmethod
    def get_regions(session):
        try:
            r_list = []  
            regions = session.query(Region).all()
            for region in regions:  
                tmp = region.to_dict()  
                obj = RegionEntity(tmp['region_id'], tmp['region_name'])  
                obj.validate()  
                r_list.append(obj)  
            return r_list  
        except Exception as e:  
            raise RegionError()
