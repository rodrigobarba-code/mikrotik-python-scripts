from .socketio_manager import SocketIOManager

def init_socketio(app):
    socketio = SocketIOManager.get_instance()
    socketio.init_app(app, async_mode='threading')

    from . import events
    events.scan_process(socketio)