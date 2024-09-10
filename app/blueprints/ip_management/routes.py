# Description: IP Addresses Routes for the IP Addresses Blueprint

# Importing Required Local Modules
from . import ip_management_bp  # Import the IP Addresses Blueprint
from models.users.functions import users_functions as functions  # Import the users functions object
# Importing Required Local Modules

# Importing Required Libraries
from flask import render_template, redirect, url_for, flash, request, jsonify, session
# Importing Required Libraries

# Importing Required Decorators
from app.decorators import RequirementsDecorators as restriction
# Importing Required Decorators

# Importing Required Models
from models.sites.models import Site
from models.regions.models import Region
from models.routers.models import Router
from models.ip_management.models import IPSegment
# Importing Required Models

# IP Addresses Main Route
@ip_management_bp.route('/', methods=['GET'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def ip_management():
    try:
        available_sites_obj = Site.get_sites()  # Get the available sites
        available_regions_obj = Region.get_regions()  # Get the available regions

        available_sites = []  # Initialize the available sites list
        available_regions = []  # Initialize the available regions list
        available_segments = []  # Initialize the available segments list

        # Loop through the available sites
        for site in available_sites_obj:
            available_sites.append({
                'id': site.site_id,  # Site ID
                'name': site.site_name,  # Site Name
                'value': site.site_name,  # Site Value
                'region': Region.get_region(site.fk_region_id).region_name,  # Region Name
                'segment': site.site_segment,  # Site Segment
                'hidden': False
            })

            available_segments.append({
                'value': site.site_segment,  # Site Value
                'segment': site.site_segment  # Site Segment
            })
        # Loop through the available sites

        # Loop through the available regions
        for region in available_regions_obj:
            available_regions.append({
                'id': region.region_id,  # Region ID
                'name': region.region_name,  # Region Name
                'value': region.region_name  # Region Value
            })
        # Loop through the available regions

        return render_template(
            'ip_management/ip_management.html',  # Render the IP Addresses template
            available_segments=available_segments,  # Pass the available segments to the template
            available_regions=available_regions,  # Pass the available regions to the template
            available_sites=available_sites  # Pass the available sites to the template
        )
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('ip_management.ip_management'))  # Redirect to the IP Addresses route
# IP Addresses Main Route

# IP Management Options by Site Route
@ip_management_bp.route('/options/<int:site_id>', methods=['GET'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def ip_management_options_by_site(site_id):
    try:
        site_id = site_id  # Get the Site ID
        site_name = Site.get_site(site_id).site_name  # Get the Site Name
        return render_template(
            'ip_management/ip_management_options.html',  # Render the IP Addresses template
            site_name=site_name,  # Pass the Site Name
            site_id=site_id  # Pass the Site ID
        )
    except Exception as e:
        flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('ip_management.ip_management'))  # Redirect to the IP Addresses route
# IP Management Options by Site Route

# IP Addresses Main w/ID Route
@ip_management_bp.route('/segments/<int:site_id>', methods=['GET'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def ip_segment(site_id):
    try:
        site_id = site_id  # Get the Site ID
        site_name = Site.get_site(site_id).site_name  # Get the Site Name
        ip_segment_list = IPSegment.get_ip_segments_by_site_id(site_id)  # Get the IP Segments by Site ID
        return render_template(
            'ip_management/ip_segments.html',  # Render the IP Addresses template
            ip_segment_list=ip_segment_list,  # Pass the IP Segments to the template
            site_name=site_name,  # Pass the Site Name to the template
            site_id=site_id  # Pass the Site ID to the template
        )
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('ip_management.ip_segment', site_id=site_id))  # Redirect to the IP Addresses route
# IP Addresses Main w/ID Route

# IP Addresses Delete Route
@ip_management_bp.route('/segments/delete/<int:segment_id>', methods=['GET'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def delete_segment(segment_id):
    try:  # Try to delete the IP Segment
        IPSegment.delete_ip_segment(segment_id)  # Delete the IP Segment
        flash('IP Segment deleted successfully', 'success')  # Flash a success message
        functions.create_log(session['user_id'], 'Router Deleted', 'DELETE', 'routers')  # Create a log
        return redirect(url_for('ip_management.ip_management'))  # Redirect to the routers route
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('ip_management.ip_management'))  # Redirect to the IP Addresses route
# IP Addresses Delete Routes

# IP Addresses Delete Bulk Route
@ip_management_bp.route('/segments/delete/bulk', methods=['POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def bulk_delete_segment():
    data = request.get_json()  # Get the JSON data
    segments_ids = data.get('items_ids', [])  # Get the routers IDs
    try:
        flag = 0  # Set the flag to 0
        for segment_id in segments_ids:  # Loop through the routers IDs
            IPSegment.delete_ip_segment(segment_id)  # Delete the IP Segment
            flag += 1  # Set the flag to 1
        flash(f'{flag} IP Segments deleted successfully', 'success')  # Flash a success message
        functions.create_log(session['user_id'], 'IP Segments Deleted', 'DELETE', 'ip_management')  # Create a log
        return jsonify({'message': 'IP Segments deleted successfully'}), 200  # Return a success message
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return jsonify({'message': 'Failed to delete IP Segments', 'error': str(e)}), 500  # Return an error message
# IP Addresses Delete Bulk Route

# IP Addresses Delete All Route
@ip_management_bp.route('/segments/delete/all', methods=['POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def delete_all_segments():
    try:  # Try to delete all IP Segments
        IPSegment.delete_all_ip_segments()  # Delete all IP Segments
        flash('All IP Segments deleted successfully', 'success')  # Flash a success message
        functions.create_log(session['user_id'], 'All IP Segments Deleted', 'DELETE', 'ip_management')  # Create a log
        return jsonify({'message': 'All IP Segments deleted successfully'}), 200  # Return a success message
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return jsonify({'message': 'Failed to delete all IP Segments', 'error': str(e)}), 500  # Return an error message
# IP Addresses Delete All Route

# IP Addresses Get IP Segments Details Route
@ip_management_bp.route('/segments/get_ip_segment_details', methods=['POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def get_ip_segment_details():
    try:
        data = request.get_json()  # Get the JSON data
        segment_id = data.get('segment_id', None)  # Get the IP Segment ID
        segment = IPSegment.get_ip_segment(segment_id)  # Get the IP Segment
        json_obj = {
            'id': segment.ip_segment_id,  # IP Segment
            'router': Router.get_router(segment.fk_router_id).router_name,  # Router Name
            'ip': segment.ip_segment_ip,  # IP Address
            'mask': segment.ip_segment_mask,  # Subnet Mask
            'network': segment.ip_segment_network,  # Network Address
            'interface': segment.ip_segment_interface,  # Interface
            'actual_iface': segment.ip_segment_actual_iface,  # Actual Interface
            'tag': segment.ip_segment_tag.value,  # Tag
            'comment': segment.ip_segment_comment,  # Comment
            'is_invalid': segment.ip_segment_is_invalid,  # Is Invalid
            'is_dynamic': segment.ip_segment_is_dynamic,  # Is Dynamic
            'is_disabled': segment.ip_segment_is_disabled  # Is Disabled
        }
        return jsonify(json_obj), 200  # Return the IP Segment data
    except Exception as e:  # If an exception occurs
        return jsonify({'message': 'Failed to get router data', 'error': str(e)}), 500  # Return an error message
# IP Addresses Get IP Segments Details Route
