from entities.router import RouterEntity
from models.routers.models import Router

class GetAllowedRouters:
    @staticmethod
    def get(session):
        try:
            routers_list = []
            routers = session.query(Router).filter(Router.allow_scan == 1).all()

            for router in routers:
                router_entity = RouterEntity(
                    router.router_id,
                    router.router_name,
                    router.router_description,
                    router.router_brand,
                    router.router_model,
                    router.fk_site_id,
                    router.router_ip,
                    router.router_mac,
                    router.router_username,
                    router.router_password,
                    router.allow_scan
                )
                routers_list.append(router_entity)
            return routers_list
        except Exception as e:
            return str("An error occurred while getting the allowed routers: " + str(e))