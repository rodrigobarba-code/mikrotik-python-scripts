# Description: IP Addresses Blueprint

# Importing Blueprint
from flask import Blueprint
# Importing Blueprint

# Defining Blueprint
ip_addresses_bp = Blueprint('ip_addresses', __name__, template_folder='templates')
# Defining Blueprint

# Importing Routes
from app.blueprints.ip_addresses import routes
# Importing Routes
