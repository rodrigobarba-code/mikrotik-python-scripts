# Importing Required Libraries
from . import notifications_bp
from flask import render_template
from app.decorators import RequirementsDecorators as restriction

# Dashboard Main Route
@notifications_bp.route('/', methods=['GET'])
@restriction.login_required  # Login Required Decorator
@restriction.redirect_to_loading_screen  # Redirect to Loading Screen Decorator
def notifications():
    return render_template('notifications/notifications.html')
