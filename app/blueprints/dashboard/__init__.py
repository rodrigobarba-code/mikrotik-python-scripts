# Importing Blueprint
from flask import Blueprint
# Importing Blueprint

# Defining Blueprint
dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')
# Defining Blueprint

# Importing Routes
from app.blueprints.dashboard import routes
# Importing Routes
