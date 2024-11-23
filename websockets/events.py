import asyncio
from api.routeros.api import RouterAPI
from websockets.socketio_manager import SocketIOManager

def scan_process(socketio) -> None:
    socketio.emit('connect')

    @socketio.on('start_scan')
    def scan_routeros():
        asyncio.run(RouterAPI.arp_scan())
        socketio.emit(
            'scan_status',
            {
                'scan_status': 'RouterOS scan initiated',
                'percent': 0
            }
        )

    @socketio.on('get_general_status')
    def scan_status_routeros():
        percent = SocketIOManager.get_percent()
        message = SocketIOManager.get_message()

        status = SocketIOManager.get_scan_status()

        socketio.emit(
            'status',
            {
                'scan_status': message,
                'percent': percent,
                'status': status
            }
        )

    @socketio.on('return_to_router_scan')
    def return_to_router_scan():
        from flask import redirect, url_for
        try:
            return redirect(url_for('router_scan.scan'))
        except Exception as e:
            return str(e)