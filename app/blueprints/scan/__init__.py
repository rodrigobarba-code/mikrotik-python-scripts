# Importing Blueprint
from flask import Blueprint
# Importing Blueprint

# Defining Blueprint
scan_bp = Blueprint('scan', __name__, template_folder='templates')
# Defining Blueprint

# Importing Routes
from app.blueprints.scan import routes
# Importing Routes
