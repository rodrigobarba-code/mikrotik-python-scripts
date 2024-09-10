from .. import Base, SessionLocal
from entities.router import RouterEntity
from sqlalchemy.orm import relationship, backref
from models.routers.functions import RoutersFunctions
from sqlalchemy import Column, Integer, String, ForeignKey

class Router(Base):
    __tablename__ = 'routers'  

    router_id = Column(Integer, primary_key=True, autoincrement=True)  
    router_name = Column(String(128), nullable=False)  
    router_description = Column(String(256), nullable=False)  
    router_brand = Column(String(128), nullable=False)  
    router_model = Column(String(128), nullable=False)  
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
            'fk_site_id': self.fk_site_id,  
            'router_ip': self.router_ip,  
            'router_mac': self.router_mac,  
            'router_username': self.router_username,  
            'router_password': self.router_password,  
            'allow_scan': self.allow_scan  
        }

    @staticmethod
    def add_router(router: RouterEntity):
        model_r = Router
        session = SessionLocal()
        v_router = RoutersFunctions()  
        try:
            if v_router.validate_router(router, 'insert', model_r):
                new_router = Router(
                    router_name=router.router_name,  
                    router_description=router.router_description,  
                    router_brand=router.router_brand,  
                    router_model=router.router_model,  
                    fk_site_id=router.fk_site_id,  
                    router_ip=router.router_ip,  
                    router_mac=router.router_mac,
                    router_username=router.router_username,  
                    router_password=router.router_password,  
                    allow_scan=router.allow_scan  
                )
                session.add(new_router)  
                session.commit()
            else:  
                raise Exception()  
        except Exception as e:  
            session.rollback()  
            raise e  

    @staticmethod
    def update_router(new_router: RouterEntity):
        model_r = Router
        session = SessionLocal()
        v_router = RoutersFunctions()  
        try:
            if v_router.validate_router(new_router, 'update', model_r):
                old_router = Router.query.get(new_router.router_id)
                old_router.router_name = new_router.router_name  
                old_router.router_description = new_router.router_description  
                old_router.router_brand = new_router.router_brand  
                old_router.router_model = new_router.router_model  
                old_router.fk_site_id = new_router.fk_site_id  
                old_router.router_ip = new_router.router_ip  
                old_router.router_mac = new_router.router_mac  
                old_router.router_username = new_router.router_username  
                old_router.router_password = new_router.router_password  
                old_router.allow_scan = new_router.allow_scan  
                session.commit()
            else:  
                raise Exception()  
        except Exception as e:  
            session.rollback()  
            raise e  

    @staticmethod
    def delete_router(router_id):
        model_r = Router
        session = SessionLocal()
        v_router = RoutersFunctions()  
        try:
            if v_router.validate_router(
                    RouterEntity(
                        router_id=router_id,  
                        router_name=str(),  
                        router_description=str(),  
                        router_brand=str(),  
                        router_model=str(),  
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
                router = Router.query.get(router_id)
                session.delete(router)  
                session.commit()
            else:  
                raise Exception()  
        except Exception as e:  
            session.rollback()  
            raise e  

    @staticmethod
    def delete_all_routers():
        session = SessionLocal()
        try:
            Router.query.delete()  
            session.commit()  
        except Exception as e:  
            session.rollback()  
            raise e
    
    @staticmethod
    def get_router(router_id):
        model_r = Router
        v_router = RoutersFunctions()  
        try:
            if v_router.validate_router(
                    RouterEntity(
                        router_id=router_id,  
                        router_name=str(),  
                        router_description=str(),  
                        router_brand=str(),  
                        router_model=str(),  
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
                router = Router.query.get(router_id)
                return router
            else:
                raise Exception()  
        except Exception as e:  
            raise e  

    @staticmethod
    def get_all_routers():
        r_list = []  
        routers = Router.query.all()  
        for router in routers:
            tmp = RouterEntity(
                router_id=router.router_id,  
                router_name=router.router_name,  
                router_description=router.router_description,  
                router_brand=router.router_brand,  
                router_model=router.router_model,  
                fk_site_id=router.fk_site_id,  
                router_ip=router.router_ip,  
                router_mac=router.router_mac,  
                router_username=router.router_username,  
                router_password=router.router_password,  
                allow_scan=router.allow_scan  
            )
            r_list.append(tmp)  
        return r_list
