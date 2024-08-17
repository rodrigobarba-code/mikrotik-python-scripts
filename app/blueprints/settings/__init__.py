# Importing Blueprint
from flask import Blueprint
# Importing Blueprint

# Defining Blueprint
settings_bp = Blueprint('settings', __name__, template_folder='templates')
# Defining Blueprint

# Importing Routes
from app.blueprints.settings import routes
# Importing Routes
