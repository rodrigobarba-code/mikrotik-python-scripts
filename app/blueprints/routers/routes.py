# Description: Routers Routes for the Routers Blueprint

# Importing Required Local Modules
from . import routers_bp  # Import the sites Blueprint
from app.blueprints.users.functions import users_functions as functions  # Import the users functions object
# Importing Required Local Modules

# Importing Required Libraries
from flask import render_template, redirect, url_for, flash, request, jsonify, session
# Importing Required Libraries

# Importing Required Decorators
from app.decorators import RequirementsDecorators as restriction
# Importing Required Decorators

# Importing Required Entities
from app.blueprints.routers.entities import RouterEntity
# Importing Required Entities

# Importing Required Models
from app.blueprints.sites.models import Site
from app.blueprints.routers.models import Router
# Importing Required Models

# Routers Main Route
@routers_bp.route('/', methods=['GET'])
@restriction.login_required  # Need to be logged in
def routers():
    try:
        router_list = Router.get_all_routers()  # Get the router list
        return render_template(
            'routers/routers.html',  # Render the routers template
            router_list=router_list,  # Pass the router list to the template
            router=None  # Pass None to the template
        )
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('routers.routers'))  # Redirect to the routers route
# Routers Main Route

# Routers Add Route
@routers_bp.route('/add', methods=['GET', 'POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required   # Need to be an admin
def add_router():
    if request.method == 'POST':  # If the request method is POST
        try:  # Try to add the router
            router = RouterEntity(  # Create a RouterEntity object
                router_id=int(),  # Set the router ID
                router_name=request.form['router_name'],  # Set the router name
                router_description=request.form['router_description'],  # Set the router description
                router_brand="Mikrotik",  # Set the router brand
                router_model=request.form['router_model'],  # Set the router model
                fk_site_id=int(request.form['fk_site_id']),  # Set the site
                router_ip=request.form['router_ip'],  # Set the router IP
                router_mac=request.form['router_mac'],  # Set the router MAC
                router_username=request.form['router_username'],  # Set the router username
                router_password=request.form['router_password'],  # Set the router password
                allow_scan=1 if request.form.get('allow_scan') else 0
            )
            router.validate()  # Validate the router
            Router.add_router(router)  # Add the router
            flash('Router added successfully', 'success')  # Flash a success message
            functions.create_log(session['user_id'], 'Router Added', 'INSERT', 'routers')  # Create a log
        except Exception as e:  # If an exception occurs
            flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('routers.routers'))  # Redirect to the routers route
    site_list = Site.get_sites()  # Get the site list
    return render_template(
        'routers/form_routers.html',  # Render the form_routers template
        site_list=site_list,  # Pass the site list to the template
        router=None  # Pass None to the template
    )
# Routers Add Route

# Routers Update Route
@routers_bp.route('/update/<int:router_id>', methods=['GET', 'POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def update_router(router_id):
    if request.method == 'POST':  # If the request method is POST
        try:  # Try to update the router
            router = RouterEntity(  # Create a RouterEntity object
                router_id=router_id,  # Set the router
                router_name=request.form['router_name'],  # Set the router name
                router_description=request.form['router_description'],  # Set the router description
                router_brand="Mikrotik",  # Set the router brand
                router_model=request.form['router_model'],  # Set the router model
                fk_site_id=int(request.form['fk_site_id']),  # Set the site
                router_ip=request.form['router_ip'],  # Set the router IP
                router_mac=request.form['router_mac'],  # Set the router MAC
                router_username=request.form['router_username'],  # Set the router username
                router_password=request.form['router_password'],  # Set the router password
                allow_scan=1 if request.form.get('allow_scan') else 0  # Set the allow scan
            )
            router.validate()  # Validate the router
            Router.update_router(router)  # Update the router
            flash('Router updated successfully', 'success')  # Flash a success message
            functions.create_log(session['user_id'], 'Router Updated', 'UPDATE', 'routers')  # Create a log
            return redirect(url_for('routers.routers'))  # Redirect to the routers route
        except Exception as e:  # If an exception occurs
            flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('routers.routers'))  # Redirect to the routers route
    site_list = Site.get_sites()  # Get the site list
    try:
        router = Router.get_router(router_id)    # Get the router
        return render_template(  # Render the form_routers template
            'routers/form_routers.html',  # Render the form_routers template
            site_list=site_list,  # Pass the site list to the template
            router=router  # Pass the router to the template
        )
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('routers.routers'))  # Redirect to the routers route
# Routers Update Route

# Routers Delete Route
@routers_bp.route('/delete/<int:router_id>', methods=['GET'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def delete_router(router_id):
    try:  # Try to delete the router
        Router.delete_router(router_id)  # Delete the router
        flash('Router Deleted Successfully', 'success')  # Flash a success message
        functions.create_log(session['user_id'], 'Router Deleted', 'DELETE', 'routers')  # Create a log
        return redirect(url_for('routers.routers'))  # Redirect to the routers route
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('routers.routers'))  # Redirect to the routers route
# Routers Delete Route

# Routers Bulk Delete Route
@routers_bp.route('/delete/bulk', methods=['POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def bulk_delete_router():
    data = request.get_json()  # Get the JSON data
    routers_ids = data.get('items_ids', [])  # Get the routers IDs
    try:
        flag = 0  # Set the flag to 0
        for router_id in routers_ids:  # Loop through the routers IDs
            Router.delete_router(router_id)  # Delete the router
            flag += 1  # Increment the flag
        flash(f'{flag} Routers deleted successfully', 'success')  # Flash a success message
        functions.create_log(session['user_id'], f'{flag} Routers Deleted', 'DELETE', 'routers')  # Create a log
        return jsonify({'message': 'Routers deleted successfully'}), 200  # Return a success message
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return jsonify({'message': 'Failed to delete routers', 'error': str(e)}), 500  # Return an error message
# Routers Bulk Delete Route

# Routers Delete All Route
@routers_bp.route('/delete/all', methods=['POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def delete_all_routers():
    try:  # Try to delete all routers
        Router.delete_all_routers()  # Delete all routers
        flash('All Routers deleted successfully', 'success')  # Flash a success message
        functions.create_log(session['user_id'], 'All Routers Deleted', 'DELETE', 'routers')  # Create a log
        return jsonify({'message': 'Routers deleted successfully'}), 200  # Return a success message
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return jsonify({'message': 'Failed to delete routers', 'error': str(e)}), 500  # Return an error message
# Routers Delete All Route

# Routers Get Router Details Route
@routers_bp.route('/get_router_details', methods=['POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def get_router_details():
    try:
        data = request.get_json()
        router_id = data.get('router_id', None)
        router = Router.get_router(router_id)
        json_obj = {
            'router_name': router.router_name,
            'router_description': router.router_description,
            'router_brand': router.router_brand,
            'router_model': router.router_model,
            'fk_site_id': Site.get_site(router.fk_site_id).site_name,
            'router_ip': router.router_ip,
            'router_mac': router.router_mac,
            'router_username': router.router_username,
            'router_password': router.router_password,
            'allow_scan': "Yes" if router.allow_scan == 1 else "No"
        }
        return jsonify(json_obj), 200
    except Exception as e:
        return jsonify({'message': 'Failed to get router data', 'error': str(e)}), 500
# Routers Get Router Details Route
