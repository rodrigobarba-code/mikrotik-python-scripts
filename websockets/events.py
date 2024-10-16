import requests
from flask_socketio import emit

def register_handlers(socketio):
    @socketio.on('start_scan')
    def handle_start_scan():
        from flask import session
        try:
            response = requests.get(
                'http://localhost:8080/routeros/private/scan/',
                params={'user_id': session.get('user_id')}
            )
            if response.status_code == 200:
                if response.json().get('backend_status') == 200:
                    emit('router_scan_finished')
                else:
                    raise Exception(response.json().get('message'))
            elif response.status_code == 500:
                raise Exception('Failed to retrieve regions')
        except Exception as e:
            emit('router_scan_failed', {'error': str(e)})
