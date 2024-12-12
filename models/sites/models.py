from .. import Base
from sqlalchemy import func, delete, text
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey

from entities.site import SiteEntity
from models.sites.exceptions import *
from models.routers.models import Router
from ..ip_management.models import IPSegment


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
    def verify_autoincrement_id(session):
        try:
            if not session.query(Site).all():
                session.execute(text("ALTER TABLE sites AUTO_INCREMENT = 1"))
        except Exception as e:
            raise SiteError()

    @staticmethod
    def add_site(session, site):
        try:
            if session.query(Site).filter(func.lower(Site.site_name) == func.lower(site.site_name)).first():
                raise SiteAlreadyExists(
                    site_id=session.query(Site).filter(
                        func.lower(Site.site_name) == func.lower(site.site_name)).first().site_id,
                    site_name=site.site_name
                )
            elif session.query(Site).filter(Site.site_segment == site.site_segment).first():
                raise SiteSameSegment(
                    site_id=session.query(Site).filter(Site.site_segment == site.site_segment).first().site_id,
                )
            else:
                new_site = Site(
                    fk_region_id=site.fk_region_id,
                    site_name=site.site_name,
                    site_segment=site.site_segment
                )
                session.add(new_site)
        except SiteSameSegment as e:
            raise e
        except SiteAlreadyExists as e:
            raise e
        except Exception as e:
            raise SiteError()

    @staticmethod
    def update_site(session, new_site):
        try:
            if not session.query(Site).get(new_site.site_id):
                raise SiteNotFound(
                    new_site.site_id
                )
            elif session.query(Site).filter(Site.site_segment == new_site.site_segment).first() and \
                    session.query(Site).filter(
                        Site.site_segment == new_site.site_segment).first().site_id != new_site.site_id:
                raise SiteSameSegment(
                    site_id=session.query(Site).filter(Site.site_segment == new_site.site_segment).first().site_id,
                )
            else:
                old_site = session.query(Site).get(new_site.site_id)
                if old_site.site_name != new_site.site_name:
                    if session.query(Site).filter(
                            func.lower(Site.site_name) == func.lower(new_site.site_name)).first() and \
                            session.query(Site).filter(func.lower(Site.site_name) == func.lower(
                                new_site.site_name)).first().site_id != new_site.site_id:
                        raise SiteAlreadyExists(
                            site_id=session.query(Site).filter(
                                func.lower(Site.site_name) == func.lower(new_site.site_name)).first().site_id,
                            site_name=new_site.site_names
                        )
                    else:
                        old_site.site_name = new_site.site_name
                        old_site.fk_region_id = new_site.fk_region_id
                        old_site.site_segment = new_site.site_segment
                        session.add(old_site)
        except SiteSameSegment as e:
            raise e
        except SiteAlreadyExists as e:
            raise e
        except SiteNotFound as e:
            raise e
        except Exception as e:
            raise SiteError()

    @staticmethod
    def delete_site(session, site_id):
        try:
            if not session.query(Site).get(site_id):
                raise SiteNotFound(site_id)
            else:
                if session.query(Router).filter(Router.fk_site_id == site_id).first():
                    raise SiteAssociatedWithRouters(
                        site_id=site_id
                    )
                else:
                    site = session.query(Site).get(site_id)
                    session.delete(site)
        except SiteAssociatedWithRouters as e:
            raise e
        except SiteNotFound as e:
            raise e
        except Exception as e:
            raise SiteError()

    @staticmethod
    def bulk_delete_sites(session, site_ids):
        try:
            if not session.query(Site).filter(Site.site_id.in_(site_ids)).all():
                raise SiteOnBulkDeleteNotFound()
            else:
                if session.query(Router).filter(Router.fk_site_id.in_(site_ids)).first():
                    raise SiteOnBulkDeleteAssociatedWithRouters
                else:
                    stmt = delete(Site).where(Site.site_id.in_(site_ids))
                    session.execute(stmt)
        except SiteOnBulkDeleteAssociatedWithRouters as e:
            raise e
        except SiteOnBulkDeleteNotFound as e:
            raise e
        except Exception as e:
            raise SiteError()

    @staticmethod
    def delete_sites(session):
        try:
            session.query(Site).delete()
        except Exception as e:
            return SiteError()

    @staticmethod
    def get_site(session, site_id):
        try:
            from models.regions.models import Region
            if not session.query(Site).get(site_id):
                raise SiteNotFound(site_id)
            else:
                join = session.query(Site, Region).join(Site, Site.fk_region_id == Region.region_id).filter(
                    Site.site_id == site_id).first()
                site_object = SiteEntity(
                    site_id=site_id,
                    fk_region_id=join.Region.region_id,
                    region_name=join.Region.region_name,
                    site_name=join.Site.site_name,
                    site_segment=join.Site.site_segment
                )
                site_object.validate()
                return site_object
        except SiteNotFound as e:
            raise e
        except Exception as e:
            raise SiteError()

    @staticmethod
    def get_sites(session):
        try:
            site_list = []
            from models.regions.models import Region
            join = session.query(Site, Region).join(Site, Site.fk_region_id == Region.region_id).all()
            for site in join:
                obj = SiteEntity(
                    site_id=site.Site.site_id,
                    fk_region_id=site.Region.region_id,
                    region_name=site.Region.region_name,
                    site_name=site.Site.site_name,
                    site_segment=site.Site.site_segment
                )
                obj.validate()
                site_list.append(obj)
            return site_list
        except Exception as e:
            raise SiteError()

    @staticmethod
    def get_available_sites(session) -> list[SiteEntity]:
        try:
            # Import the necessary models
            from models.routers.models import Router
            from models.regions.models import Region

            # Create a list for the available sites
            available_sites = []

            # Get all the sites
            sites = session.query(Site).all()

            # Iterate over the sites
            for site in sites:
                # Verify if the site is associated with a router
                if not session.query(Router).filter(Router.fk_site_id == site.site_id).first():
                    # Get the region name
                    region = session.query(Region).filter(Region.region_id == site.fk_region_id).first()

                    # Append the site to the list
                    available_sites.append(SiteEntity(
                        site_id=site.site_id,
                        fk_region_id=site.fk_region_id,
                        region_name=region.region_name,
                        site_name=site.site_name,
                        site_segment=site.site_segment
                    ))

            # Return the available sites
            return available_sites
        except Exception as e:
            raise SiteError()

    @staticmethod
    def bulk_insert_sites(session, sites: list[SiteEntity]) -> None:
        """
        Bulk insert sites into the database
        :param session: SQLAlchemy session
        :param sites: List of sites to be inserted
        :return: None
        """

        try:
            # Create a list for the sites
            site_list = []

            # Iterate over the list of sites
            for site in sites:
                # Verify if the site already exists
                if not session.query(Site).filter(
                        func.lower(Site.site_name) == func.lower(site.site_name)).first():
                    # Append the site to the list
                    site_list.append(Site(
                        fk_region_id=site.fk_region_id,
                        site_name=site.site_name,
                        site_segment=site.site_segment
                    ))

            # Bulk insert the sites
            session.bulk_save_objects(site_list)
        except Exception as e:
            # Raise the exception
            raise e

    @staticmethod
    def get_sites_with_segments(session):
        from models.ip_management.models import IPSegment

        try:
            # Get the sites
            sites = session.query(Site).all()

            # Create a list for the sites
            site_list = []

            # Iterate over the sites
            for site in sites:
                # Obtain the routers associated with the site
                router = session.query(Router).filter(Router.fk_site_id == site.site_id).first()
                # Obtain the segments associated with the router
                segment_list = session.query(IPSegment).filter(IPSegment.fk_router_id == router.router_id).all()

                # If the segment list is not empty, append the site to the list
                if len(segment_list) > 0:
                    site_list.append(SiteEntity(
                        site_id=site.site_id,
                        fk_region_id=site.fk_region_id,
                        region_name=str(),
                        site_name=site.site_name,
                        site_segment=site.site_segment
                    ))

                else:
                    continue

            # Return the list of sites
            return site_list
        except Exception as e:
            raise SiteError()
