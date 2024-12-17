from api.routeros.modules.allowed_routers import AllowedRouters


class QueueList(AllowedRouters):
    queue_list = []

    def __init__(self):
        pass

    @staticmethod
    def _obtain_by_router(router: object):
        try:
            queue_list = {}

            response = router.talk('/queue/simple/print')
            for queue in response:
                if queue['disabled'] == 'false':
                    queue_list[queue['name']] = queue['target'].split('/')[0]
            return queue_list
        except Exception as e:
            return f'Error on _obtain_by_router: {e}'

    @staticmethod
    def _get_alias(ip: str, queue_list: dict) -> str:
        try:
            for key, value in queue_list.items():
                if ip == key:
                    return str(value)
            else:
                return 'No Alias'
        except Exception as e:
            return f'Error on _get_alias: {e}'
