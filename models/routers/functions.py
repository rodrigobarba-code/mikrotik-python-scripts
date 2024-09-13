import re
import ipaddress
from sqlalchemy import func

from models.routers.exceptions import *

class RoutersFunctions:
    def __init__(self):  
        pass  

    @staticmethod
    def validate_ip(ip):
        try:
            ipaddress.ip_address(ip)  
            return True  
        except ValueError:
            return False  

    @staticmethod
    def validate_mac(mac):
        try:
            if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
                return True  
            else:
                return False  
        except ValueError:
            return False  

    @staticmethod
    def validate_router(session, router, operation, model) -> bool:
        try:
            if operation in ["insert", "update"]:  
                if operation == "update":  
                    existing_router = session.query(model).get(router.router_id)
                    if not existing_router:  
                        raise RouterNotFound(router.router_id)  
                
                if session.query(model).filter(func.lower(model.router_name) == func.lower(router.router_name)).first() and \
                        session.query(model).filter(func.lower(model.router_name) == func.lower(router.router_name)).first().router_id != router.router_id:
                    raise RouterAlreadyExists(  
                        router_id=session.query(model).filter(
                            func.lower(model.router_name) == func.lower(router.router_name)).first().router_id,
                        router_name=router.router_name  
                    )
                
                if not RoutersFunctions.validate_ip(router.router_ip):
                    raise RouterIPNotValid(router.router_ip)  
                
                if not RoutersFunctions.validate_mac(router.router_mac):
                    raise RouterMACNotValid(router.router_mac)  
                
                if session.query(model).filter(func.lower(model.router_ip) == func.lower(router.router_ip)).first() and \
                        session.query(model).filter(func.lower(model.router_ip) == func.lower(router.router_ip)).first().router_id != router.router_id:
                    raise RouterIPAlreadyExists(  
                        router_id=session.query(model).filter(
                            func.lower(model.router_ip) == func.lower(router.router_ip)).first().router_id,
                        router_ip=router.router_ip  
                    )
                
                if session.query(model).filter(func.lower(model.router_mac) == func.lower(router.router_mac)).first() and \
                        session.query(model).filter(func.lower(model.router_mac) == func.lower(router.router_mac)).first().router_id != router.router_id:
                    raise RouterMACAlreadyExists(  
                        router_id=session.query(model).filter(
                            func.lower(model.router_mac) == func.lower(router.router_mac)).first().router_id,
                        router_mac=router.router_mac  
                    )
                return True  
            
            elif operation in ["delete", "get"]:  
                if not session.query(model).filter(model.router_id == router.router_id).first():
                    raise RouterNotFound(router.router_id)  
                return True  
            return False  
        except (RouterNotFound, RouterIPNotValid, RouterMACNotValid, RouterAlreadyExists, RouterIPAlreadyExists,
                RouterMACAlreadyExists) as e:  
            raise e  
        except Exception:  
            raise RouterError()  

    @staticmethod
    def validate_bulk_delete(session, model, router_ids):
        try:
            if not session.query(model).filter(model.router_id.in_(router_ids)).all():
                raise RouterNotFound(router_ids)
            return True
        except RouterNotFound as e:
            raise e
        except Exception:
            raise RouterError()
