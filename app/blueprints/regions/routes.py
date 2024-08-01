# Description: Regions Routes for the Region Blueprint

# Importing Required Libraries
from flask import render_template, redirect, url_for, flash, request, jsonify
# Importing Required Libraries

# Importing Required Decorators
from app.decorators import RequirementsDecorators as restriction
# Importing Required Decorators

# Importing Required Entities
from app.blueprints.regions.entities import RegionEntity
# Importing Required Entities

# Importing Required Models
from app.blueprints.regions.models import Region
# Importing Required Models

from . import regions_bp  # Import the regions Blueprint

# Regions Main Route
@regions_bp.route('/', methods=['GET'])
@restriction.login_required  # Need to be logged in
def regions():
    try:
        region_list = Region.get_regions()  # Get all regions on the database
        return render_template(
            'regions/regions.html',  # Render the regions template
            region_list=region_list, region=None  # Pass the region list and None to the template
        )
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('regions.regions'))  # Redirect to the regions route
# Regions Main Route

# Regions Add Route
@regions_bp.route('/add', methods=['GET', 'POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def add_region():
    if request.method == 'POST':  # If the request method is POST
        try:  # Try to add the region
            region = RegionEntity(  # Create a RegionEntity object
                region_id=int(),  # Set the region ID
                region_name=request.form['region_name']  # Set the region name
            )
            Region.add_region(region)  # Add the region
            flash('Region added successfully', 'success')  # Flash a success message
        except Exception as e:  # If an exception occurs
            flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('regions.regions'))  # Redirect to the regions route
    return render_template(
        'regions/form_regions.html',  # Render the form_regions template
        region=None  # Pass None to the template
    )
# Regions Add Route

# Regions Update Route
@regions_bp.route('/update/<int:region_id>', methods=['GET', 'POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def update_region(region_id):
    if request.method == 'POST':  # If the request method is POST
        try:  # Try to update the region
            region = RegionEntity(  # Create a RegionEntity object
                region_id=region_id,  # Set the region ID
                region_name=request.form['region_name']  # Set the region name
            )
            Region.update_region(region)  # Update the region
            flash('Region was updated successfully', 'success')  # Flash a success message
        except Exception as e:  # If an exception occurs
            flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('regions.regions'))  # Redirect to the regions route
    try:  # Try to get the region
        region = Region.get_region(region_id)  # Get the region by Identifier
        return render_template(
            'regions/form_regions.html',  # Render the form_regions template
            region=region  # Pass the region to the template
        )
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('regions.regions'))  # Redirect to the regions route
# Regions Update Route

# Regions Delete Route
@regions_bp.route('/delete/<int:region_id>', methods=['GET'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def delete_region(region_id):
    try:  # Try to delete the region
        Region.delete_region(region_id)  # Delete the region
        flash('Region deleted successfully', 'success')  # Flash a success message
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
    return redirect(url_for('regions.regions'))  # Redirect to the regions route
# Regions Delete Route
