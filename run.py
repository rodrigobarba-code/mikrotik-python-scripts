# Importing Eventlet
import eventlet.wsgi  # Importing eventlet.wsgi
eventlet.monkey_patch()  # Patching the eventlet
# Importing Eventlet

# Importing main application constructor
from app import create_app
from flask_caching import Cache
from app.config import AppConfig, Sidebar
from app.blueprints.scan.routes import socketio
# Importing main application constructor

el = eventlet  # Assigning eventlet to el
app = create_app()  # Creating application instance
socketio.init_app(app)  # Initializing the socketio
cache = Cache(app, config={'CACHE_TYPE': 'simple'})  # Initializing the cache

# Injecting global variables into the context
@app.context_processor
@cache.cached(timeout=600)
def injects():
    return dict(
        metadata=AppConfig.METADATA,  # Injecting metadata into the context
        menu_items=Sidebar.menu_items,  # Injecting menu items into the context
        profile_menu_items=Sidebar.profile_menu_items  # Injecting profile menu items into the context
    )
# Injecting global variables into the context

# Running application
if __name__ == '__main__':
    socketio.run(
        app,  # Running the application
        port=AppConfig.PORT,  # Running the app on the specified port
        debug=AppConfig.DEBUG,  # Running the app in debug mode
        allow_unsafe_werkzeug=True  # Allowing unsafe werkzeug
    )
# Running application
