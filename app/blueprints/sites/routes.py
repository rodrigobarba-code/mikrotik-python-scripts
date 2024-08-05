# Description: Sites Routes for the Site Blueprint

# Importing Required Local Modules
from app.blueprints.users.functions import users_functions as functions  # Import the users functions object
from . import sites_bp  # Import the sites Blueprint
# Importing Required Local Modules

# Importing Required Libraries
from flask import render_template, redirect, url_for, flash, request, jsonify, session
# Importing Required Libraries

# Importing Required Decorators
from app.decorators import RequirementsDecorators as restriction
# Importing Required Decorators

# Importing Required Entities
from app.blueprints.sites.entities import SiteEntity
# Importing Required Entities

# Importing Required Models
from app.blueprints.sites.models import Site
from app.blueprints.regions.models import Region
# Importing Required Models

# Sites Main Route
@sites_bp.route('/', methods=['GET'])
@restriction.login_required  # Need to be logged in
def sites():
    try:
        site_list = Site.get_sites()  # Get the site list
        region_functions = Region()  # Create a Region object
        return render_template(
            'sites/sites.html',  # Render the sites template
            region_functions=region_functions,  # Pass the region object to the template
            site_list=site_list,  # Pass the site list to the template
            site=None  # Pass None to the template
        )
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('sites.sites'))  # Redirect to the sites route
# Sites Main Route

# Sites Add Route
@sites_bp.route('/add', methods=['GET', 'POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def add_site():
    if request.method == 'POST':  # If the request method is POST
        try:  # Try to add the site
            site = SiteEntity(  # Create a SitesEntity object
                site_id=int(),  # Set the site ID
                site_name=request.form['site_name'],  # Set the site name
                fk_region_id=int(request.form['fk_region_id']),  # Set the region
                site_segment=int(request.form['site_segment'])  # Set the site segment
            )
            Site.add_site(site)  # Add the site
            flash('Site added successfully', 'success')  # Flash a success message
            functions.create_log(session['user_id'], 'Site Added', 'INSERT', 'sites')  # Create a log
        except Exception as e:  # If an exception occurs
            flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('sites.sites'))  # Redirect to the sites route
    region_list = Region.get_regions()  # Get the region list
    return render_template(
        'sites/form_sites.html',  # Render the form_sites template
        region_list=region_list,  # Pass the region list to the template
        site=None  # Pass None to the template
    )
# Sites Add Route

# Sites Update Route
@sites_bp.route('/update/<int:site_id>', methods=['GET', 'POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def update_site(site_id):
    if request.method == 'POST':  # If the request method is POST
        try:  # Try to update the site
            site = SiteEntity(  # Create a SitesEntity object
                site_id=site_id,  # Set the site ID
                site_name=request.form['site_name'],  # Set the site name
                fk_region_id=int(request.form['fk_region_id']),  # Set the region
                site_segment=int(request.form['site_segment'])  # Set the site segment
            )
            Site.update_site(site)  # Update the site
            flash('Site updated successfully', 'success')  # Flash a success message
            functions.create_log(session['user_id'], 'Site Updated', 'UPDATE', 'sites')  # Create a log
        except Exception as e:  # If an exception occurs
            flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('sites.sites'))  # Redirect to the sites route
    try:  # Try to get the site
        site = Site.get_site(site_id)  # Get the site
        region_list = Region.get_regions()  # Get the region list
        return render_template(
            'sites/form_sites.html',  # Render the form_sites template
            region_list=region_list,  # Pass the region list to the template
            site=site  # Pass the site to the template
        )
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('sites.sites'))  # Redirect to the sites route
# Sites Update Route

# Sites Delete Route
@sites_bp.route('/delete/<int:site_id>', methods=['GET'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def delete_site(site_id):
    try:  # Try to delete the site
        Site.delete_site(site_id)  # Delete the site
        flash('Site deleted successfully', 'success')  # Flash a success message
        functions.create_log(session['user_id'], 'Site Deleted', 'DELETE', 'sites')  # Create a log
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
    return redirect(url_for('sites.sites'))  # Redirect to the sites route
# Sites Delete Route

# Sites Bulk Delete Route
@sites_bp.route('/delete/bulk', methods=['POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def bulk_delete_site():
    data = request.get_json()  # Get the JSON data
    sitess_ids = data.get('items_ids', [])  # Get the sites IDs
    try:
        flag = 0  # Set the flag to 0
        for site_id in sitess_ids:  # Loop through the sites IDs
            Site.delete_site(site_id)  # Delete the site
            flag += 1  # Increment the flag
        flash(f'{flag} Sites Deleted Successfully', 'success')  # Flash a success message
        functions.create_log(session['user_id'], f'{flag} Sites Deleted', 'DELETE', 'sites')  # Create a log
        return jsonify({'message': 'Sites deleted successfully'}), 200  # Return a success message
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return jsonify({'message': 'Failed to delete sites', 'error': str(e)}), 500
# Sites Bulk Delete Route

# Sites Delete All Route
@sites_bp.route('/delete/all', methods=['POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def delete_all_sites():
    try:  # Try to delete all sites
        Site.delete_all_sites()  # Delete all sites
        flash('All Sites Deleted Successfully', 'success')  # Flash a success message
        functions.create_log(session['user_id'], 'All Sites Deleted', 'DELETE', 'sites')  # Create a log
        return jsonify({'message': 'Sites deleted successfully'}), 200  # Return a success message
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return jsonify({'message': 'Failed to delete sites', 'error': str(e)}), 500  # Return an error message
# Sites Delete All Route
