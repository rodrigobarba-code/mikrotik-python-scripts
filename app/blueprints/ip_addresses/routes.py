# Description: IP Addresses Routes for the IP Addresses Blueprint

# Importing Required Local Modules
from . import ip_addresses_bp  # Import the IP Addresses Blueprint
# Importing Required Local Modules

# Importing Required Libraries
from flask import render_template, redirect, url_for, flash, request, jsonify, session
# Importing Required Libraries

# Importing Required Decorators
from app.decorators import RequirementsDecorators as restriction
# Importing Required Decorators

# Importing Required Entities

# Importing Required Entities

# Importing Required Models

# Importing Required Models

# IP Addresses Main Route
@ip_addresses_bp.route('/ip-addresses', methods=['GET'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def ip_addresses():
    try:
        return render_template(
            'ip_addresses/ip_addresses.html',  # Render the IP Addresses template
            ip_address_list=None  # Pass None to the template
        )
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('ip_addresses.ip_addresses'))  # Redirect to the IP Addresses route
# IP Addresses Main Route
