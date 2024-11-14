from .. import Base
from sqlalchemy import text
from entities.router import RouterEntity
from sqlalchemy.orm import relationship, backref
from models.routers.functions import RoutersFunctions
from sqlalchemy import Column, Integer, String, ForeignKey, delete

class Router(Base):
    __tablename__ = 'routers'  

    router_id = Column(Integer, primary_key=True, autoincrement=True)  
    router_name = Column(String(128), nullable=False)  
    router_description = Column(String(256), nullable=False)  
    router_brand = Column(String(128), nullable=False)  
    router_model = Column(String(128), nullable=False)
    router_serial = Column(String(128), nullable=True)
    fk_site_id = Column(Integer, ForeignKey('sites.site_id'), nullable=False)  
    router_ip = Column(String(16), nullable=False)  
    router_mac = Column(String(32), nullable=False)  
    router_username = Column(String(128), nullable=False)  
    router_password = Column(String(128), nullable=False)  
    allow_scan = Column(Integer, nullable=False, default=0)
    
    site = relationship('Site', backref=backref('routers', lazy=True))  

    def __repr__(self):
        return f'<Router {self.router_id}>'  

    def to_dict(self):
        return {
            'router_id': self.router_id,  
            'router_name': self.router_name,  
            'router_description': self.router_description,  
            'router_brand': self.router_brand,  
            'router_model': self.router_model,
            'router_serial': self.router_serial,
            'fk_site_id': self.fk_site_id,  
            'router_ip': self.router_ip,  
            'router_mac': self.router_mac,  
            'router_username': self.router_username,  
            'router_password': self.router_password,  
            'allow_scan': self.allow_scan  
        }

    @staticmethod
    def verify_autoincrement_id(session):
        try:
            if not session.query(Router).all():
                session.execute(text("ALTER TABLE routers AUTO_INCREMENT = 1"))
        except Exception as e:
            raise e

    @staticmethod
    def add_router(session, router: RouterEntity):
        model_r = Router
        v_router = RoutersFunctions()  
        try:
            if v_router.validate_router(session, router, 'insert', model_r):
                new_router = Router(
                    router_name=router.router_name,  
                    router_description=router.router_description,  
                    router_brand=router.router_brand,  
                    router_model=router.router_model,
                    router_serial=router.router_serial,
                    fk_site_id=router.fk_site_id,  
                    router_ip=router.router_ip,  
                    router_mac=router.router_mac,
                    router_username=router.router_username,  
                    router_password=router.router_password,  
                    allow_scan=router.allow_scan  
                )
                session.add(new_router)
            else:  
                raise Exception()  
        except Exception as e:
            raise e  

    @staticmethod
    def update_router(session, new_router: RouterEntity):
        model_r = Router
        v_router = RoutersFunctions()  
        try:
            if v_router.validate_router(session, new_router, 'update', model_r):
                old_router = session.query(Router).get(new_router.router_id)
                old_router.router_name = new_router.router_name  
                old_router.router_description = new_router.router_description  
                old_router.router_brand = new_router.router_brand  
                old_router.router_model = new_router.router_model
                old_router.router_serial = new_router.router_serial
                old_router.fk_site_id = new_router.fk_site_id  
                old_router.router_ip = new_router.router_ip  
                old_router.router_mac = new_router.router_mac  
                old_router.router_username = new_router.router_username  
                old_router.router_password = new_router.router_password  
                old_router.allow_scan = new_router.allow_scan
            else:  
                raise Exception()  
        except Exception as e:
            raise e  

    @staticmethod
    def delete_router(session, router_id):
        model_r = Router
        v_router = RoutersFunctions()  
        try:
            if v_router.validate_router(
                    session,
                    RouterEntity(
                        router_id=router_id,  
                        router_name=str(),  
                        router_description=str(),  
                        router_brand=str(),  
                        router_model=str(),  
                        router_serial=str(),
                        fk_site_id=int(),
                        router_ip=str(),  
                        router_mac=str(),  
                        router_username=str(),  
                        router_password=str(),  
                        allow_scan=int()  
                    ),
                    'delete',  
                    model_r  
            ):
                router = session.query(Router).get(router_id)
                session.delete(router)
            else:  
                raise Exception()  
        except Exception as e:
            raise e

    @staticmethod
    def bulk_delete_routers(session, router_ids):
        model_r = Router
        v_router = RoutersFunctions()
        try:
            if v_router.validate_bulk_delete(session, model_r, router_ids):
                stmt = delete(Router).where(Router.router_id.in_(router_ids))
                session.execute(stmt)
        except Exception as e:
            raise e

    @staticmethod
    def delete_routers(session):
        try:
            session.query(Router).delete()
        except Exception as e:
            raise e
    
    @staticmethod
    def get_router(session, router_id):
        model_r = Router
        v_router = RoutersFunctions()  
        try:
            if v_router.validate_router(
                    session,
                    RouterEntity(
                        router_id=router_id,  
                        router_name=str(),  
                        router_description=str(),  
                        router_brand=str(),  
                        router_model=str(),
                        router_serial=str(),
                        fk_site_id=int(),  
                        router_ip=str(),  
                        router_mac=str(),  
                        router_username=str(),  
                        router_password=str(),  
                        allow_scan=int()  
                    ),
                    'get',  
                    model_r  
            ):
                router = session.query(Router).get(router_id)
                return router
            else:
                raise Exception()  
        except Exception as e:  
            raise e  

    @staticmethod
    def get_routers(session):
        r_list = []  
        routers = session.query(Router).all()
        for router in routers:
            tmp = RouterEntity(
                router_id=router.router_id,  
                router_name=router.router_name,  
                router_description=router.router_description,  
                router_brand=router.router_brand,  
                router_model=router.router_model,
                router_serial=router.router_serial,
                fk_site_id=router.fk_site_id,  
                router_ip=router.router_ip,  
                router_mac=router.router_mac,  
                router_username=router.router_username,  
                router_password=router.router_password,  
                allow_scan=router.allow_scan  
            )
            r_list.append(tmp)  
        return r_list

    @staticmethod
    def allow_scan_all(session):
        try:
            for router in session.query(Router).all():
                router.allow_scan = 1
        except Exception as e:
            raise e

    @staticmethod
    def deny_scan_all(session):
        try:
            for router in session.query(Router).all():
                router.allow_scan = 0
        except Exception as e:
            raise e

    @staticmethod
    def bulk_insert_routers(session, routers: list[RouterEntity]) -> None:
        """
        Bulk insert routers into the database
        :param session: SQLAlchemy session
        :param routers: List of RouterEntity objects
        :return: None
        """

        # Import RouterAPI class
        from api.routeros.api import RouterAPI

        # Create a model object
        model_r = Router

        # Create an instance of the RoutersFunctions class
        v_router = RoutersFunctions()

        try:
            # Create a list to store the new routers
            router_list = []

            # Iterate for the RouterEntity objects list
            for router in routers:
                # Validate if the router information is correct
                if v_router.validate_router(session, router, 'insert', model_r):
                    # Create a new Router object
                    new_router = Router(
                        router_name=router.router_name,
                        router_description=router.router_description,
                        router_brand=router.router_brand,
                        router_model=router.router_model,
                        router_serial=router.router_serial,
                        fk_site_id=router.fk_site_id,
                        router_ip=router.router_ip,
                        router_mac=router.router_mac,
                        router_username=router.router_username,
                        router_password=router.router_password,
                        allow_scan=router.allow_scan
                    )
                    # Create a new RouterAPI object
                    # print(router.router_ip, router.router_username, router.router_password)

                    router_api_obj = RouterAPI(
                        router.router_ip,
                        router.router_username,
                        router.router_password
                    )

                    # Set the RouterAPI object to the new router
                    router_api_obj.set_api()

                    # Verify the router credentials
                    flag = RouterAPI.verify_router_connection(router_api_obj.get_api())

                    if flag is True:
                        # Append the new router to the list
                        router_list.append(new_router)
                    else:
                        # Raise an exception
                        raise Exception('The Router with IP: ' + new_router.router_ip + ' is not reachable')
                else:
                    # If not exception is raised, raise a new exception
                    raise Exception()

            # Bulk save the new routers
            session.bulk_save_objects(router_list)
        except Exception as e:
            # Raise the exception
            raise e
