# Importing Blueprint
from flask import Blueprint
# Importing Blueprint

# Defining Blueprint
auth_bp = Blueprint('auth', __name__, template_folder='templates')
# Defining Blueprint

# Importing Routes
from app.blueprints.auth import routes
# Importing Routes
