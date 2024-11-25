from app import create_app  # Import the create_app function from the app package

# Import the necessary classes and functions from the Flask and threading packages
from threading import Thread
from websockets.socketio_manager import SocketIOManager
from app.config import AppConfig, UserJobs, Sidebar

# Create the Flask app using the create_app function
flask_app = create_app()

# Get the SocketIO instance from the SocketIOManager class
socketio = SocketIOManager.get_instance()

# Inject the metadata into the Flask app for use in on all templates
@flask_app.context_processor
def injects():
    return dict(
        metadata=AppConfig.METADATA,
        menu_items=Sidebar.menu_items,
        job_display=UserJobs.job_display,
        profile_menu_items=Sidebar.profile_menu_items
    )

# Function to start the Flask app, and running it with a web socket
def start_flask():
    socketio.run(
        flask_app,
        use_reloader=False,
        debug=AppConfig.DEBUG,
        allow_unsafe_werkzeug=True,
        host="0.0.0.0", port=AppConfig.PORT
    )

# Start the Flask app in a separate thread
if __name__ == "__main__":
    thread = Thread(target=start_flask)
    thread.start()
    thread.join()