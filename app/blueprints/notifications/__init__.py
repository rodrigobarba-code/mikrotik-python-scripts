# Importing Blueprint
from flask import Blueprint
# Importing Blueprint

# Defining Blueprint
notifications_bp = Blueprint('notifications', __name__, template_folder='templates')
# Defining Blueprint

# Importing Routes
from app.blueprints.notifications import routes
# Importing Routes
