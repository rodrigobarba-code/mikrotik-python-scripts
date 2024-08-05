# Description: Sites Blueprint

# Importing Blueprint
from flask import Blueprint
# Importing Blueprint

# Defining Blueprint
sites_bp = Blueprint('sites', __name__, template_folder='templates')
# Defining Blueprint

# Importing Routes
from app.blueprints.sites import routes
# Importing Routes
