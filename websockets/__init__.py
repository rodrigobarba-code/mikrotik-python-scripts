from flask_socketio import SocketIO

socketio = SocketIO()

def init_socketio(app):
    socketio.init_app(app, async_mode='threading')

    from . import events
    events.register_handlers(socketio)
