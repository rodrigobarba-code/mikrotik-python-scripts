# Importing necessary modules
from flask import render_template, redirect, url_for, flash, request, session
# Importing necessary modules

# Importing necessary decorators
from app.decorators import RequirementsDecorators as restriction
# Importing necessary decorators

# Importing necessary models

# Importing necessary models

from . import scan_bp  # Importing the blueprint instance

# Scan Main Route
@scan_bp.route('/scan', methods=['GET', 'POST'])
def scan():
    return render_template('scan/scan.html')
# Scan Main Route
