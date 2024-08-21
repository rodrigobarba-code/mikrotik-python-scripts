# Description: IP Addresses Routes for the IP Addresses Blueprint

# Importing Required Local Modules
from . import ip_addresses_bp  # Import the IP Addresses Blueprint
from app.blueprints.users.functions import users_functions as functions  # Import the users functions object
# Importing Required Local Modules

# Importing Required Libraries
from flask import render_template, redirect, url_for, flash, request, jsonify, session
# Importing Required Libraries

# Importing Required Decorators
from app.decorators import RequirementsDecorators as restriction
# Importing Required Decorators

# Importing Required Models
from app.blueprints.routers.models import Router
from app.blueprints.ip_addresses.models import IPSegment
# Importing Required Models

# IP Addresses Main Route
@ip_addresses_bp.route('/', methods=['GET'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def ip_addresses():
    try:
        ip_segment_list = IPSegment.get_ip_segments()  # Get the IP Segments

        return render_template(
            'ip_addresses/ip_addresses.html',  # Render the IP Addresses template
            ip_segment_list=ip_segment_list  # IP Segment List
        )
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('ip_addresses.ip_addresses'))  # Redirect to the IP Addresses route
# IP Addresses Main Route

# IP Addresses Delete Route
@ip_addresses_bp.route('/delete/<int:segment_id>', methods=['GET'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def delete_segment(segment_id):
    try:  # Try to delete the IP Segment
        IPSegment.delete_ip_segment(segment_id)  # Delete the IP Segment
        flash('IP Segment deleted successfully', 'success')  # Flash a success message
        functions.create_log(session['user_id'], 'Router Deleted', 'DELETE', 'routers')  # Create a log
        return redirect(url_for('ip_addresses.ip_addresses'))  # Redirect to the routers route
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return redirect(url_for('ip_addresses.ip_addresses'))  # Redirect to the IP Addresses route
# IP Addresses Delete Routes

# IP Addresses Delete Bulk Route
@ip_addresses_bp.route('/delete/bulk', methods=['POST'])
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
        functions.create_log(session['user_id'], 'IP Segments Deleted', 'DELETE', 'ip_addresses')  # Create a log
        return jsonify({'message': 'IP Segments deleted successfully'}), 200  # Return a success message
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return jsonify({'message': 'Failed to delete IP Segments', 'error': str(e)}), 500  # Return an error message
# IP Addresses Delete Bulk Route

# IP Addresses Delete All Route
@ip_addresses_bp.route('/delete/all', methods=['POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def delete_all_segments():
    try:  # Try to delete all IP Segments
        IPSegment.delete_all_ip_segments()  # Delete all IP Segments
        flash('All IP Segments deleted successfully', 'success')  # Flash a success message
        functions.create_log(session['user_id'], 'All IP Segments Deleted', 'DELETE', 'ip_addresses')  # Create a log
        return jsonify({'message': 'All IP Segments deleted successfully'}), 200  # Return a success message
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return jsonify({'message': 'Failed to delete all IP Segments', 'error': str(e)}), 500  # Return an error message
# IP Addresses Delete All Route

# IP Addresses Get IP Segments Details Route
@ip_addresses_bp.route('/get_ip_segment_details', methods=['POST'])
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
        return jsonify({'message': 'IP Segment data retrieved successfully', 'data': json_obj}), 200  # Return the IP Segment data
    except Exception as e:  # If an exception occurs
        return jsonify({'message': 'Failed to get router data', 'error': str(e)}), 500  # Return an error message
# IP Addresses Get IP Segments Details Route
