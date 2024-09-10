from flask_socketio import SocketIO  # Import the SocketIO class

socketio = SocketIO()  # Create an instance of the SocketIO class

def init_socketio(app):
    # Initialize and configure Socket.IO with Flask
    socketio.init_app(app, async_mode='threading')

    # Import and register the event handlers
    from . import events
    events.register_handlers(socketio)
