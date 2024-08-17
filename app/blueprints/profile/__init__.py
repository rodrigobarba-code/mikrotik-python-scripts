# Importing Blueprint
from flask import Blueprint
# Importing Blueprint

# Defining Blueprint
profile_bp = Blueprint('profile', __name__, template_folder='templates')
# Defining Blueprint

# Importing Routes
from app.blueprints.profile import routes
# Importing Routes
