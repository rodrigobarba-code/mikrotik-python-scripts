# Description: Users Blueprint

# Importing Blueprint
from flask import Blueprint
# Importing Blueprint

# Defining Blueprint
routers_bp = Blueprint('routers', __name__, template_folder='templates')
# Defining Blueprint

# Importing Routes
from app.blueprints.routers import routes
# Importing Routes
