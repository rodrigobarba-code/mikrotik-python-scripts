# Importing Blueprint
from flask import Blueprint
# Importing Blueprint

# Defining Blueprint
regions_bp = Blueprint('regions', __name__, template_folder='templates')
# Defining Blueprint

# Importing Routes
from app.blueprints.region import routes
# Importing Routes
