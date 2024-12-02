# Importing Flask, Configurations and App Extensions
from flask import Flask
from app.config import AppConfig
from app.functions import functions
from websockets import init_socketio
# Importing Flask, Configurations and App Extensions

# Importing Blueprints
from app.blueprints.home import home_bp
from app.blueprints.auth import auth_bp
from app.blueprints.sites import sites_bp
from app.blueprints.users import users_bp
from app.blueprints.routers import routers_bp
from app.blueprints.regions import regions_bp
from app.blueprints.profile import profile_bp
from app.blueprints.router_scan import scan_bp
from app.blueprints.settings import settings_bp
from app.blueprints.dashboard import dashboard_bp
from app.blueprints.notifications import notifications_bp
from app.blueprints.ip_management import ip_management_bp
# Importing Blueprints

# Function constructor to create the app
def create_app():
    app = Flask(__name__)  # Creating the app instance

    app.config.from_object(AppConfig)  # Setting the application configurations
    init_socketio(app)  # Initializing the socketio

    # Registering the blueprints
    app.register_blueprint(home_bp, url_prefix='/')  # Registering the home blueprint
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Registering the auth blueprint
    app.register_blueprint(sites_bp, url_prefix='/sites')  # Registering the sites blueprint
    app.register_blueprint(users_bp, url_prefix='/users')  # Registering the users blueprint
    app.register_blueprint(profile_bp, url_prefix='/profile')  # Registering the profile blueprint
    app.register_blueprint(routers_bp, url_prefix='/routers')  # Registering the routers blueprint
    app.register_blueprint(regions_bp, url_prefix='/regions')  # Registering the regions blueprint
    app.register_blueprint(scan_bp, url_prefix='/router/scan')  # Registering the router_scan blueprint
    app.register_blueprint(settings_bp, url_prefix='/settings')  # Registering the settings blueprint
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')  # Registering the dashboard blueprint
    app.register_blueprint(notifications_bp, url_prefix='/notifications')  # Registering the notifications blueprint
    app.register_blueprint(ip_management_bp, url_prefix='/ip/management')  # Registering the ip_management blueprint
    # Registering the blueprints

    return app  # Returning the app
# Function constructor to create the app
