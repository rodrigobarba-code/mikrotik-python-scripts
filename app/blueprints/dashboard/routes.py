# Importing Required Libraries
from . import dashboard_bp
from flask import render_template
from app.decorators import RequirementsDecorators as restriction
# Importing Required Libraries

# Dashboard Main Route
@dashboard_bp.route('/', methods=['GET'])
@restriction.login_required  # Login Required Decorator
@restriction.admin_required  # Admin Required Decorator
def dashboard():
    return render_template('dashboard/dashboard.html')  # Rendering Dashboard Template
# Dashboard Main Route
