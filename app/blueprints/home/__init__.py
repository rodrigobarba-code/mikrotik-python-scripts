# Importing Blueprint
from flask import Blueprint
# Importing Blueprint

# Defining Blueprint
home_bp = Blueprint('home', __name__, template_folder='templates')
# Defining Blueprint

# Importing Routes
from app.blueprints.home import routes
# Importing Routes
