# Importing Required Libraries
from . import profile_bp
from flask import render_template, redirect, url_for, flash, request, jsonify
from app.decorators import RequirementsDecorators as restriction


# Importing Required Libraries

# Home Main Route
@profile_bp.route('/', methods=['GET'])
@restriction.login_required
def profile():
    return render_template('profile/profile.html')
# Home Main Route
