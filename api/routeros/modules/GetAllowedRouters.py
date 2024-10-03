from models.routers.models import Router

class GetAllowedRouters:
    @staticmethod
    def get(session) -> list[dict]:
        try:
            router_list = []
            routers = session.query(Router).filter(Router.allow_scan == 1).all()

            for router in routers:
                router_dict = {
                    'id': router.router_id,
                    'ip': router.router_ip,
                    'mac': router.router_mac,
                    'username': router.router_username,
                    'password': router.router_password
                }
                router_list.append(router_dict)
            return router_list
        except Exception as e:
            raise e
