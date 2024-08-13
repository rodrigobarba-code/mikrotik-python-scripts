# Importing Flask, Configurations and App Extensions
from flask import Flask
from app.functions import functions
from app.extensions import db, migrate
from app.config import DatabaseConfig, AppConfig
# Importing Flask, Configurations and App Extensions

# Importing Blueprints
from app.blueprints.home import home_bp
from app.blueprints.auth import auth_bp
from app.blueprints.scan import scan_bp
from app.blueprints.sites import sites_bp
from app.blueprints.users import users_bp
from app.blueprints.routers import routers_bp
from app.blueprints.regions import regions_bp
from app.blueprints.dashboard import dashboard_bp
# Importing Blueprints

# Function constructor to create the app
def create_app():
    app = Flask(__name__)  # Creating the app

    app.config.from_object(AppConfig)  # Setting the application configurations
    app.config.from_object(DatabaseConfig)  # Setting the database configurations

    db.init_app(app)  # Initializing the database
    migrate.init_app(app, db)  # Initializing the migration

    # Registering the blueprints
    app.register_blueprint(home_bp, url_prefix='/')  # Registering the home blueprint
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Registering the auth blueprint
    app.register_blueprint(scan_bp, url_prefix='/router')  # Registering the scan blueprint
    app.register_blueprint(sites_bp, url_prefix='/sites')  # Registering the sites blueprint
    app.register_blueprint(users_bp, url_prefix='/users')  # Registering the users blueprint
    app.register_blueprint(routers_bp, url_prefix='/routers')  # Registering the routers blueprint
    app.register_blueprint(regions_bp, url_prefix='/regions')  # Registering the regions blueprint
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')  # Registering the dashboard blueprint
    # Registering the blueprints

    return app  # Returning the app
# Function constructor to create the app
