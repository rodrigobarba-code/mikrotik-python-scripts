"""
# Version: 1.0
This module initializes the SocketIOManager and the events that will be used in the application.
The init_socketio function initializes the SocketIOManager and the events that will be used in the application.
"""

# Import the SocketIOManager class from the socketio_manager module
from .socketio_manager import SocketIOManager

# Function to initialize the SocketIOManager and the events that will be used in the application
def init_socketio(app) -> None:

    # Get the instance of the SocketIOManager
    socketio = SocketIOManager.get_instance()

    # Initialize the SocketIOManager with the Flask app
    socketio.init_app(app, async_mode='threading')

    # Import the events module and call the scan_process function to initialize the events
    from . import events
    events.scan_process(socketio)
