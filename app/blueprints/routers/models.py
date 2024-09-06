# Description: Router Model for the Router Blueprint

# Importing Required Libraries
from app.extensions import db
# Importing Required Libraries

# Importing Required Entities
from app.blueprints.routers.entities import RouterEntity
# Importing Required Entities

# Importing Required Functions
from app.blueprints.routers.functions import RoutersFunctions
# Importing Required Functions

# Router Model
class Router(db.Model):
    __tablename__ = 'routers'  # Table Name

    # Columns
    router_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary Key
    router_name = db.Column(db.String(128), nullable=False)  # Router Name
    router_description = db.Column(db.String(256), nullable=False)  # Router Description
    router_brand = db.Column(db.String(128), nullable=False)  # Router Brand
    router_model = db.Column(db.String(128), nullable=False)  # Router Model
    fk_site_id = db.Column(db.Integer, db.ForeignKey('sites.site_id'), nullable=False)  # Foreign Key
    router_ip = db.Column(db.String(16), nullable=False)  # Router IP
    router_mac = db.Column(db.String(32), nullable=False)  # Router MAC
    router_username = db.Column(db.String(128), nullable=False)  # Router Username
    router_password = db.Column(db.String(128), nullable=False)  # Router Password
    allow_scan = db.Column(db.Integer, nullable=False, default=0)  # Allow Scan
    # Columns

    # Relationships
    site = db.relationship('Site', backref=db.backref('routers', lazy=True))  # Site Relationship
    # Relationships

    # Object Representation
    def __repr__(self):
        return f'<Router {self.router_id}>'  # Router Object Representation
    # Object Representation

    # Dictionary Representation
    def to_dict(self):
        return {
            'router_id': self.router_id,  # Router ID
            'router_name': self.router_name,  # Router Name
            'router_description': self.router_description,  # Router Description
            'router_brand': self.router_brand,  # Router Brand
            'router_model': self.router_model,  # Router Model
            'fk_site_id': self.fk_site_id,  # Foreign Key
            'router_ip': self.router_ip,  # Router IP
            'router_mac': self.router_mac,  # Router MAC
            'router_username': self.router_username,  # Router Username
            'router_password': self.router_password,  # Router Password
            'allow_scan': self.allow_scan  # Allow Scan
        }
    # Dictionary Representation

    # Static Methods
    # Router - Add Router
    @staticmethod
    def add_router(router: RouterEntity):
        model_r = Router  # Router Model
        v_router = RoutersFunctions()  # Router Functions Instance
        try:
            # Check if the router information is valid
            if v_router.validate_router(router, 'insert', model_r):
                # If everything is valid, add the router to the database
                # Create a new Router object
                new_router = Router(
                    router_name=router.router_name,  # Router Name
                    router_description=router.router_description,  # Router Description
                    router_brand=router.router_brand,  # Router Brand
                    router_model=router.router_model,  # Router Model
                    fk_site_id=router.fk_site_id,  # Foreign Key
                    router_ip=router.router_ip,  # Router IP
                    router_mac=router.router_mac,
                    router_username=router.router_username,  # Router Username
                    router_password=router.router_password,  # Router Password
                    allow_scan=router.allow_scan  # Allow Scan
                )
                db.session.add(new_router)  # Add the new router to the session
                db.session.commit()  # Commit the changes
                # If everything is valid, add the router to the database
            else:  # If the router information is not valid
                raise Exception()  # Raise an exception
        except Exception as e:  # If any other exception occurs
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
    # Router - Add Router

    # Router - Update Router
    @staticmethod
    def update_router(new_router: RouterEntity):
        model_r = Router  # Router Model
        v_router = RoutersFunctions()  # Router Functions Instance
        try:
            # Check if the router information is valid
            if v_router.validate_router(new_router, 'update', model_r):
                # If everything is valid, update the router in the database
                # Get the router that will be updated
                old_router = Router.query.get(new_router.router_id)
                # Update the router information
                old_router.router_name = new_router.router_name  # Router Name
                old_router.router_description = new_router.router_description  # Router Description
                old_router.router_brand = new_router.router_brand  # Router Brand
                old_router.router_model = new_router.router_model  # Router Model
                old_router.fk_site_id = new_router.fk_site_id  # Foreign Key
                old_router.router_ip = new_router.router_ip  # Router IP
                old_router.router_mac = new_router.router_mac  # Router MAC
                old_router.router_username = new_router.router_username  # Router Username
                old_router.router_password = new_router.router_password  # Router Password
                old_router.allow_scan = new_router.allow_scan  # Allow Scan
                db.session.commit()  # Commit the changes
                # If everything is valid, update the router in the database
            else:  # If the router information is not valid
                raise Exception()  # Raise an exception
        except Exception as e:  # If any other exception occurs
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
    # Router - Update Router

    # Router - Delete Router
    @staticmethod
    def delete_router(router_id):
        model_r = Router  # Router Model
        v_router = RoutersFunctions()  # Router Functions Instance
        try:
            # Check if the router information is valid
            if v_router.validate_router(
                    RouterEntity(
                        router_id=router_id,  # Router ID
                        router_name=str(),  # Router Name
                        router_description=str(),  # Router Description
                        router_brand=str(),  # Router Brand
                        router_model=str(),  # Router Model
                        fk_site_id=int(),  # Foreign Key
                        router_ip=str(),  # Router IP
                        router_mac=str(),  # Router MAC
                        router_username=str(),  # Router Username
                        router_password=str(),  # Router Password
                        allow_scan=int()  # Allow Scan
                    ),
                    'delete',  # Operation
                    model_r  # Site Model
            ):
                # If everything is valid, delete the router from the database
                # Get the router that will be deleted
                router = Router.query.get(router_id)
                db.session.delete(router)  # Delete the router
                db.session.commit()  # Commit the changes
                # If everything is valid, delete the router from the database
            else:  # If the router information is not valid
                raise Exception()  # Raise an exception
        except Exception as e:  # If any other exception occurs
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
    # Router - Delete Router

    # Router - Delete All Routers
    @staticmethod
    def delete_all_routers():
        try:
            Router.query.delete()  # Delete all routers
            db.session.commit()  # Commit the changes
        except Exception as e:  # If any other exception occurs
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
    # Router - Delete All Routers

    # Router - Get Router
    @staticmethod
    def get_router(router_id):
        model_r = Router  # Router Model
        v_router = RoutersFunctions()  # Router Functions Instance
        try:
            # Check if the router information is valid
            if v_router.validate_router(
                    RouterEntity(
                        router_id=router_id,  # Router ID
                        router_name=str(),  # Router Name
                        router_description=str(),  # Router Description
                        router_brand=str(),  # Router Brand
                        router_model=str(),  # Router Model
                        fk_site_id=int(),  # Foreign Key
                        router_ip=str(),  # Router IP
                        router_mac=str(),  # Router MAC
                        router_username=str(),  # Router Username
                        router_password=str(),  # Router Password
                        allow_scan=int()  # Allow Scan
                    ),
                    'get',  # Operation
                    model_r  # Site Model
            ):
                # If everything is valid, get the router from the database
                # Get the router
                router = Router.query.get(router_id)
                return router  # Return the router
                # If everything is valid, get the router from the database
            else:  # If the router information is not valid
                raise Exception()  # Raise an exception
        except Exception as e:  # If any other exception occurs
            raise e  # Raise the exception
    # Router - Get Router

    # Router - Get All Routers
    @staticmethod
    def get_all_routers():
        r_list = []  # Router List
        routers = Router.query.all()  # Get all routers
        for router in routers:  # For each router
            # Create a new RouterEntity object
            tmp = RouterEntity(
                router_id=router.router_id,  # Router ID
                router_name=router.router_name,  # Router Name
                router_description=router.router_description,  # Router Description
                router_brand=router.router_brand,  # Router Brand
                router_model=router.router_model,  # Router Model
                fk_site_id=router.fk_site_id,  # Foreign Key
                router_ip=router.router_ip,  # Router IP
                router_mac=router.router_mac,  # Router MAC
                router_username=router.router_username,  # Router Username
                router_password=router.router_password,  # Router Password
                allow_scan=router.allow_scan  # Allow Scan
            )
            r_list.append(tmp)  # Append the RouterEntity object to the Router List
        return r_list  # Return the Router List
    # Router - Get All Routers
# Router Model
