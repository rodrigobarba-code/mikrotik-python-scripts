# Description: Site Model for the Site Blueprint

# Importing Required Libraries
from app.extensions import db
from app.extensions import func
# Importing Required Libraries

# Importing Required Entities
from app.blueprints.sites.entities import SiteEntity
# Importing Required Entities

# Importing Required Models
from app.blueprints.routers.models import Router
# Importing Required Models

# Importing Required Exceptions
from app.blueprints.sites.exceptions import *
# Importing Required Exceptions

# Sites Model
class Site(db.Model):
    __tablename__ = 'sites'  # Table Name

    # Columns
    site_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary Key
    fk_region_id = db.Column(db.Integer, db.ForeignKey('regions.region_id'), nullable=False)  # Foreign Key
    site_name = db.Column(db.String(128), nullable=False)  # Site Name
    site_segment = db.Column(db.Integer, nullable=False)  # Site Segment
    # Columns

    # Relationships
    region = db.relationship('Region', backref=db.backref('sites', lazy=True))  # Region Relationship
    # Relationships

    # Object Representation
    def __repr__(self):
        return f'<Site {self.site_id}>'  # Site Object Representation
    # Object Representation

    # Dictionary Representation
    def to_dict(self):
        return {
            'site_id': self.site_id,  # Site ID
            'fk_region_id': self.fk_region_id,  # Foreign Key Region ID
            'site_name': self.site_name,  # Site Name
            'site_segment': self.site_segment  # Site Segment
        }
    # Dictionary Representation

    # Static Methods
    # Site - Add Site
    @staticmethod
    def add_site(site):
        try:
            # Check if the site name already exists
            if Site.query.filter(func.lower(Site.site_name) == func.lower(site.site_name)).first():
                # Raise SiteAlreadyExists Exception
                raise SiteAlreadyExists(
                    site_id=Site.query.filter(func.lower(Site.site_name) == func.lower(site.site_name)).first().site_id,  # Site ID
                    site_name=site.site_name  # Site Name
                )
            # Check if the site segment already exists
            elif Site.query.filter(Site.site_segment == site.site_segment).first():
                # Raise SiteSameSegment Exception
                raise SiteSameSegment(
                    site_id=Site.query.filter(Site.site_segment == site.site_segment).first().site_id,  # Site ID
                )
            else:
                # Create a new Site object
                new_site = Site(
                    fk_region_id=site.fk_region_id,  # Foreign Key Region ID
                    site_name=site.site_name,  # Site Name
                    site_segment=site.site_segment  # Site Segment
                )
                db.session.add(new_site)  # Add the new site to the session
                db.session.commit()  # Commit the session
        except SiteSameSegment as e:  # If the site segment already exists
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
        except SiteAlreadyExists as e:  # If the site already exists
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
        except Exception as e:  # If any other exception occurs
            db.session.rollback()  # Rollback the session
            raise SiteError()  # Raise SiteError Exception
    # Site - Add Site

    # Site - Update Site
    @staticmethod
    def update_site(new_site):
        try:
            # Check if the site that will be updated exists
            if not Site.query.get(new_site.site_id):
                # If the site does not exist, raise SiteNotFound Exception
                raise SiteNotFound(
                    new_site.site_id  # Site ID
                )
            # Check if the site segment already exists
            elif Site.query.filter(Site.site_segment == new_site.site_segment).first():
                # Raise SiteSameSegment Exception
                raise SiteSameSegment(
                    site_id=Site.query.filter(Site.site_segment == new_site.site_segment).first().site_id,  # Site ID
                )
            else:
                # If the site exists, update it
                old_site = db.session.query(Site).get(new_site.site_id)

                if old_site.site_name != new_site.site_name:
                    # Check if the site name already exists
                    if Site.query.filter(func.lower(Site.site_name) == func.lower(new_site.site_name)).first():
                        # If the site name already exists, raise SiteAlreadyExists Exception
                        raise SiteAlreadyExists(
                            # Site ID
                            site_id=Site.query.filter(func.lower(Site.site_name) == func.lower(new_site.site_name)).first().site_id,
                            # Site Name
                            site_name=new_site.site_names
                        )
                    else:
                        # Update the site
                        old_site.site_name = new_site.site_name  # Site Name
                        old_site.fk_region_id = new_site.fk_region_id  # Foreign Key Region ID
                        old_site.site_segment = new_site.site_segment  # Site Segment
                        db.session.add(old_site)  # Add the updated site to the session
                        db.session.commit()  # Commit the session
                        # Update the site
                # If the site exists, update it
        except SiteSameSegment as e:  # If the site segment already exists
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
        except SiteAlreadyExists as e:  # If the site already exists
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
        except SiteNotFound as e:
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
        except Exception as e:  # If any other exception occurs
            db.session.rollback()  # Rollback the session
            raise SiteError()  # Raise SiteError Exception
    # Site - Update Site

    # Site - Delete Site
    @staticmethod
    def delete_site(site_id):
        try:
            # Check if the site exists
            if not Site.query.get(site_id):
                # If the site does not exist, raise SiteNotFound Exception
                raise SiteNotFound(site_id)
            else:
                # Verify if the site is associated with at least one router
                if db.session.query(Router).filter(Router.fk_site_id == site_id).first():
                    # If the site is associated with a region, raise SiteAssociatedWithRouters Exception
                    raise SiteAssociatedWithRouters(
                        site_id=site_id  # Site ID
                    )
                else:
                    # If the site exists and is not associated with a router, delete it
                    site = Site.query.get(site_id)  # Get the site by ID
                    db.session.delete(site)  # Delete the site
                    db.session.commit()  # Commit the session
                    # If the site exists and is not associated with a router, delete it
        except SiteAssociatedWithRouters as e:  # If the site is associated with a router
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
        except SiteNotFound as e:  # If the site does not exist
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
        except Exception as e:  # If any other exception occurs
            db.session.rollback()  # Rollback the session
            raise SiteError()  # Raise SiteError Exception
    # Site - Delete Site

    # Sites - Delete All Sites
    @staticmethod
    def delete_all_sites():
        try:
            Site.query.delete()  # Delete all sites
            db.session.commit()  # Commit the session
        except Exception as e:
            db.session.rollback()  # Rollback the session
            return SiteError()  # Raise SiteError Exception
    # Sites - Delete All Sites

    # Site - Get Site
    @staticmethod
    def get_site(site_id):
        try:
            # Check if the site exists
            if not Site.query.get(site_id):
                # If the site does not exist, raise SiteNotFound Exception
                raise SiteNotFound(site_id)
            else:
                # If the site exists, return it
                tmp = Site.query.get_or_404(
                    site_id).to_dict()  # Get the site by ID and convert it to a dictionary
                site = SiteEntity(
                    int(tmp['site_id']),  # Site ID
                    int(tmp['fk_region_id']),  # Foreign Key Region ID
                    tmp['site_name'],  # Site Name
                    int(tmp['site_segment'])  # Site Segment
                )  # Create a SiteEntity object
                site.validate()  # Validate the Site Entity
                return site  # Return the Site Entity
                # If the region exists, return it
        except SiteNotFound as e:  # If the site does not exist
            raise e  # Raise the exception
        except Exception as e:  # If any other exception occurs
            raise SiteError()
    # Site - Get Site

    # Site - Get Sites
    @staticmethod
    def get_sites():
        try:
            r_list = []  # Create a list to store the sites
            sites = Site.query.all()  # Get all sites
            for site in sites:  # For each site
                tmp = site.to_dict()  # Convert the site to a dictionary
                obj = SiteEntity(
                    int(tmp['site_id']),  # Site ID
                    int(tmp['fk_region_id']),  # Foreign Key Region ID
                    tmp['site_name'],  # Site Name
                    int(tmp['site_segment'])  # Site Segment
                )  # Create a SiteEntity object
                obj.validate()  # Validate the Site Entity
                r_list.append(obj)  # Append the SiteEntity object to the list
            return r_list  # Return the list
        except Exception as e:  # If any exception occurs
            raise SiteError()  # Raise SiteError Exception
    # Site - Get Sites
    # Static Methods
# Site Model
