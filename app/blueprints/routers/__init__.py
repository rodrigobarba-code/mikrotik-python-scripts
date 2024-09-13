from flask import Blueprint

routers_bp = Blueprint('routers', __name__, template_folder='templates')

from app.blueprints.routers import routes