# Importing Required Libraries
from . import settings_bp
from flask import render_template, redirect, url_for, flash, request, jsonify
from app.decorators import RequirementsDecorators as restriction


# Importing Required Libraries

# Home Main Route
@settings_bp.route('/', methods=['GET'])
@restriction.login_required
def settings():
    return render_template('settings/settings.html')
# Home Main Route
