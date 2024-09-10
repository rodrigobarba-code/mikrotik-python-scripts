from sqlalchemy import func
from .. import Base, SessionLocal
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey

from entities.site import SiteEntity
from models.sites.exceptions import *

class Site(Base):
    __tablename__ = 'sites'
    
    site_id = Column(Integer, primary_key=True, autoincrement=True)  
    fk_region_id = Column(Integer, ForeignKey('regions.region_id'), nullable=False)  
    site_name = Column(String(128), nullable=False)  
    site_segment = Column(Integer, nullable=False)  

    region = relationship('Region', backref=backref('sites', lazy=True))  

    def __repr__(self):
        return f'<Site {self.site_id}>'

    def to_dict(self):
        return {
            'site_id': self.site_id,  
            'fk_region_id': self.fk_region_id,  
            'site_name': self.site_name,  
            'site_segment': self.site_segment  
        }

    @staticmethod
    def add_site(site):
        session = SessionLocal()
        try:
            if Site.query.filter(func.lower(Site.site_name) == func.lower(site.site_name)).first():
                raise SiteAlreadyExists(
                    site_id=Site.query.filter(func.lower(Site.site_name) == func.lower(site.site_name)).first().site_id,  
                    site_name=site.site_name  
                )
            elif Site.query.filter(Site.site_segment == site.site_segment).first():
                
                raise SiteSameSegment(
                    site_id=Site.query.filter(Site.site_segment == site.site_segment).first().site_id,  
                )
            else:
                new_site = Site(
                    fk_region_id=site.fk_region_id,  
                    site_name=site.site_name,  
                    site_segment=site.site_segment  
                )
                session.add(new_site)  
                session.commit()  
        except SiteSameSegment as e:  
            session.rollback()  
            raise e  
        except SiteAlreadyExists as e:  
            session.rollback()  
            raise e  
        except Exception as e:  
            session.rollback()  
            raise SiteError()
    
    @staticmethod
    def update_site(new_site):
        session = SessionLocal()
        try:
            if not Site.query.get(new_site.site_id):
                raise SiteNotFound(
                    new_site.site_id  
                )
            elif Site.query.filter(Site.site_segment == new_site.site_segment).first() and \
                    Site.query.filter(Site.site_segment == new_site.site_segment).first().site_id != new_site.site_id:
                raise SiteSameSegment(
                    site_id=Site.query.filter(Site.site_segment == new_site.site_segment).first().site_id,  
                )
            else:
                old_site = session.query(Site).get(new_site.site_id)
                if old_site.site_name != new_site.site_name:
                    if Site.query.filter(func.lower(Site.site_name) == func.lower(new_site.site_name)).first() and \
                            Site.query.filter(func.lower(Site.site_name) == func.lower(new_site.site_name)).first().site_id != new_site.site_id:
                        raise SiteAlreadyExists(
                            site_id=Site.query.filter(func.lower(Site.site_name) == func.lower(new_site.site_name)).first().site_id,
                            
                            site_name=new_site.site_names
                        )
                    else:
                        old_site.site_name = new_site.site_name  
                        old_site.fk_region_id = new_site.fk_region_id  
                        old_site.site_segment = new_site.site_segment  
                        session.add(old_site)  
                        session.commit()
        except SiteSameSegment as e:  
            session.rollback()  
            raise e  
        except SiteAlreadyExists as e:  
            session.rollback()  
            raise e  
        except SiteNotFound as e:
            session.rollback()  
            raise e  
        except Exception as e:  
            session.rollback()  
            raise SiteError()  

    @staticmethod
    def delete_site(site_id, model):
        session = SessionLocal()
        try:
            if not Site.query.get(site_id):
                raise SiteNotFound(site_id)
            else:
                if session.query(model).filter(model.fk_site_id == site_id).first():
                    raise SiteAssociatedWithRouters(
                        site_id=site_id  
                    )
                else:
                    site = Site.query.get(site_id)  
                    session.delete(site)  
                    session.commit()
        except SiteAssociatedWithRouters as e:  
            session.rollback()  
            raise e  
        except SiteNotFound as e:  
            session.rollback()  
            raise e  
        except Exception as e:  
            session.rollback()  
            raise SiteError()

    @staticmethod
    def delete_all_sites(model):
        session = SessionLocal()
        try:
            for site in Site.query.all():
                if session.query(model).filter(model.fk_site_id == site.site_id).first():
                    raise SiteAssociatedWithRouters(
                        site_id=site.site_id  
                    )
                else:
                    session.delete(site)  
                    session.commit()
        except Exception as e:
            session.rollback()  
            return SiteError()  

    @staticmethod
    def get_site(site_id):
        try:
            if not Site.query.get(site_id):
                raise SiteNotFound(site_id)
            else:
                tmp = Site.query.get_or_404(
                    site_id).to_dict()  
                site = SiteEntity(
                    int(tmp['site_id']),  
                    int(tmp['fk_region_id']),  
                    tmp['site_name'],  
                    int(tmp['site_segment'])  
                )  
                site.validate()  
                return site
        except SiteNotFound as e:  
            raise e  
        except Exception as e:  
            raise SiteError()

    @staticmethod
    def get_sites():
        try:
            r_list = []  
            sites = Site.query.all()  
            for site in sites:  
                tmp = site.to_dict()  
                obj = SiteEntity(
                    int(tmp['site_id']),  
                    int(tmp['fk_region_id']),  
                    tmp['site_name'],  
                    int(tmp['site_segment'])  
                )  
                obj.validate()  
                r_list.append(obj)  
            return r_list  
        except Exception as e:  
            raise SiteError()  
