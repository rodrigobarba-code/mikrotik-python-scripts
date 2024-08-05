# Importing main application constructor
from app import create_app
from flask_caching import Cache
from app.config import AppConfig, Sidebar
# Importing main application constructor

app = create_app()  # Creating application instance
cache = Cache(app, config={'CACHE_TYPE': 'simple'})  # Initializing the cache

# Injecting global variables into the context
@app.context_processor
@cache.cached(timeout=600)
def injects():
    return dict(
        menu_items=Sidebar.menu_items,  # Injecting menu items into the context
        profile_menu_items=Sidebar.profile_menu_items  # Injecting profile menu items into the context
    )
# Injecting global variables into the context

# Running application
if __name__ == '__main__':
    app.run(
        port=AppConfig.PORT,  # Running the app on port 5000
        debug=AppConfig.DEBUG  # Running the app in debug mode
    )  # Running the app with the configurations
# Running application
