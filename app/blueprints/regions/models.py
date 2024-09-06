# Description: Region Model for the Region Blueprint

# Importing Required Libraries
from app.extensions import db
from app.extensions import func
# Importing Required Libraries

# Importing Required Entities
from app.blueprints.regions.entities import RegionEntity
# Importing Required Entities

# Importing Required Models
from app.blueprints.sites.models import Site
# Importing Required Models

# Importing Required Exceptions
from app.blueprints.regions.exceptions import *
# Importing Required Exceptions

# Region Model
class Region(db.Model):
    __tablename__ = 'regions'  # Table Name

    # Columns
    region_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary Key
    region_name = db.Column(db.String(128), nullable=False)  # Region Name
    # Columns

    # Object Representation
    def __repr__(self):
        return f'<Region {self.region_id}>'  # Region Object Representation
    # Object Representation

    # Dictionary Representation
    def to_dict(self):
        return {
            'region_id': self.region_id,  # Region ID
            'region_name': self.region_name  # Region Name
        }
    # Dictionary Representation

    # Static Methods
    # Region - Add Region
    @staticmethod
    def add_region(region):
        try:
            # Check if the region name already exists
            if Region.query.filter(func.lower(Region.region_name) == func.lower(region.region_name)).first():
                # Raise RegionAlreadyExists Exception
                raise RegionAlreadyExists(
                    region_id=Region.query.filter(func.lower(Region.region_name) == func.lower(region.region_name)).first().region_id,  # Region ID
                    region_name=region.region_name  # Region Name
                )
            else:
                # Create a new Region object
                new_region = Region(
                    region_name=region.region_name  # Region Name
                )
                region.validate()  # Validate the Region Entity
                db.session.add(new_region)  # Add the new region to the session
                db.session.commit()  # Commit the session
        except RegionAlreadyExists as e:  # If the region already exists
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
        except Exception as e:  # If any other exception occurs
            db.session.rollback()  # Rollback the session
            raise RegionError()  # Raise RegionError Exception
    # Region - Add Region

    # Region - Update Region
    @staticmethod
    def update_region(new_region):
        try:
            # Check if the region that will be updated exists
            if not Region.query.get(new_region.region_id):
                # If the region does not exist, raise RegionNotFound Exception
                raise RegionNotFound(
                    new_region.region_id  # Region ID
                )
            else:
                # If the region exists, update it
                old_region = db.session.query(Region).get(new_region.region_id)  # Get the region by ID

                if old_region.region_name != new_region.region_name:
                    # Check if the region name already exists
                    if Region.query.filter(func.lower(Region.region_name) == func.lower(new_region.region_name)).first():
                        # If the region name already exists, raise RegionAlreadyExists Exception
                        raise RegionAlreadyExists(
                            # Region ID
                            region_id=Region.query.filter(func.lower(Region.region_name) == func.lower(new_region.region_name)).first().region_id,
                            # Region Name
                            region_name=new_region.region_name
                        )
                    else:
                        # Update the region
                        old_region.region_name = new_region.region_name
                        db.session.add(old_region)  # Add the updated region to the session
                        db.session.commit()  # Commit the session
                # If the region exists, update it
        except RegionAlreadyExists as e:  # If the region already exists
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
        except RegionNotFound as e:  # If the region does not exist
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
        except Exception as e:  # If any exception occurs
            db.session.rollback()  # Rollback the session
            raise RegionError()  # Raise RegionError Exception
    # Region - Update Region

    # Region - Delete Region
    @staticmethod
    def delete_region(region_id):
        try:
            # Check if the region exists
            if not Region.query.get(region_id):
                # If the region does not exist, raise RegionNotFound Exception
                raise RegionNotFound(region_id)
            else:
                # Verify if the region is associated with a router
                if db.session.query(Site).filter(Site.fk_region_id == region_id).first():
                    # If the region is associated with a site, raise RegionAssociatedWithSite Exception
                    raise RegionAssociatedWithSite(
                        region_id=region_id,  # Region ID
                        site_id=db.session.query(Site).filter(Site.fk_region_id == region_id).first().site_id  # Site ID
                    )
                else:
                    # If the region exists, delete it
                    region = Region.query.get(region_id)  # Get the region by ID
                    db.session.delete(region)  # Delete the region
                    db.session.commit()  # Commit the session
                # If the region exists, delete it
        except RegionAssociatedWithSite as e:  # If the region is associated with a site
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
        except RegionNotFound as e:  # If the region does not exist
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
        except Exception as e:  # If any exception occurs
            db.session.rollback()  # Rollback the session
            raise RegionError()  # Raise RegionError Exception
    # Region - Delete Region

    # Region - Delete All Regions
    @staticmethod
    def delete_all_regions():
        try:
            Region.query.delete()  # Delete all regions
            db.session.commit()  # Commit the session
        except Exception as e:
            db.session.rollback()  # Rollback the session
            raise RegionError()  # Raise RegionError Exception
    # Region - Delete All Regions

    # Region - Get Region
    @staticmethod
    def get_region(region_id):
        try:
            # Check if the region exists
            if not Region.query.get(region_id):
                # If the region does not exist, raise RegionNotFound Exception
                raise RegionNotFound(region_id)
            else:
                # If the region exists, return it
                tmp = Region.query.get_or_404(region_id).to_dict()  # Get the region by ID and convert it to a dictionary
                region = RegionEntity(
                    tmp['region_id'],  # Region ID
                    tmp['region_name']  # Region Name
                )
                region.validate()  # Validate the Region Entity
                return region  # Return the Region Entity
                # If the region exists, return it
        except RegionNotFound as e:  # If the region does not exist
            raise e  # Raise the exception
        except Exception as e:  # If any exception occurs
            raise RegionError()  # Raise RegionError Exception
    # Region - Get Region

    # Region - Get Regions
    @staticmethod
    def get_regions():
        try:
            r_list = []  # Create a list to store the regions
            regions = Region.query.all()  # Get all regions
            for region in regions:  # For each region
                tmp = region.to_dict()  # Convert the region to a dictionary
                obj = RegionEntity(tmp['region_id'], tmp['region_name'])  # Create a RegionEntity object
                obj.validate()  # Validate the Region Entity
                r_list.append(obj)  # Append the RegionEntity object to the list
            return r_list  # Return the list
        except Exception as e:  # If any exception occurs
            raise RegionError()  # Raise RegionError Exception
    # Region - Get Regions
    # Static Methods
# Region Model
