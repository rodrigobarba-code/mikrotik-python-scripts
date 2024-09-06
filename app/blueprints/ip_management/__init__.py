# Description: IP Management Blueprint

# Importing Blueprint
from flask import Blueprint
# Importing Blueprint

# Defining Blueprint
ip_management_bp = Blueprint('ip_management', __name__, template_folder='templates')
# Defining Blueprint

# Importing Routes
from app.blueprints.ip_management import routes
# Importing Routes
