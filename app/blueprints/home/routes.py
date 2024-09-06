# Importing Required Libraries
from . import home_bp
from flask import render_template
from app.decorators import RequirementsDecorators as restriction
# Importing Required Libraries

# Home Main Route
@home_bp.route('/', methods=['GET'])
@restriction.login_required
def home():
    return render_template('home/home.html')  # Rendering Home Page
# Home Main Route
