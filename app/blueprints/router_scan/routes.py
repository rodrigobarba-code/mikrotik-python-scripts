# Description: Scanning Routes for the Scan Blueprint

# Importing necessary modules
import time
import eventlet
from flask_socketio import SocketIO
from flask import render_template, request, redirect, url_for, flash, session, jsonify
# Importing necessary modules

# Importing Required Local Modules
from models.users.functions import users_functions as functions  # Import the users functions object
# Importing Required Local Modules

# Importing Router API
from api.routeros.api import RouterAPI
# Importing Router API

# Importing Required Decorators
from app.decorators import RequirementsDecorators as restriction
# Importing Required Decorators

# Importing necessary entities

# Importing necessary entities

# Importing necessary models
from models.router_scan.models import ARP, ARPTags
from models.ip_management.models import IPSegment
# Importing necessary models

from . import scan_bp  # Importing the blueprint instance

socketio = SocketIO()  # Initializing the socketio instance

# Scan Main Route
@scan_bp.route('/', methods=['GET', 'POST'])
def scan():
    # ARP.delete_all_arps()
    # ARPTags.delete_all_arp_tags()

    arp_dict = []  # ARP dictionary
    arp_list = ARP.get_arps()  # Getting the ARP list
    for arp in arp_list:
        arp_dict.append({
            'id': arp.arp_id,
            'ip': arp.arp_ip,
            'mac': arp.arp_mac,
            'segment': str(IPSegment.query.get(arp.fk_ip_address_id).ip_segment_ip + "/" + IPSegment.query.get(arp.fk_ip_address_id).ip_segment_mask),
            'interface': arp.arp_interface,
            'alias': arp.arp_alias,
            'tag': ARPTags.get_arp_tags(arp.arp_id)
        })
    return render_template(
        'router_scan/scan.html',  # Rendering the router_scan template
        arp_list=[] if arp_dict is None else arp_dict,  # ARP list
    )  # Rendering Router Scan Template
# Scan Main Route

# Scan Delete Route
@scan_bp.route('/delete/<int:arp_id>', methods=['GET'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def delete_arp_ip(arp_id):
    try:  # Try to delete the ARP IP
        ARPTags.delete_arp_tags(arp_id)  # Delete the ARP Tags
        ARP.delete_arp(arp_id)  # Delete the ARP IP
        flash('ARP IP Deleted Successfully', 'success')  # Flash a success message
        functions.create_log(session['user_id'], 'ARP IP Deleted', 'DELETE', 'router_scan')  # Create a log
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
    return redirect(url_for('router_scan.router_scan'))  # Redirect to the router_scan route
# Scan Delete Route

# Scan Bulk Delete Route
@scan_bp.route('/delete/bulk', methods=['POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def bulk_delete_arp_ips():
    data = request.get_json()  # Get the JSON data
    arps_ids = data.get('items_ids', [])  # Get the ARP IDs
    try:
        flag = 0  # Set the flag to 0
        for arp_id in arps_ids:  # Loop through the ARP IDs
            ARPTags.delete_arp_tags(arp_id)  # Delete the ARP Tags
            ARP.delete_arp(arp_id)  # Delete the ARP IP
            flag += 1  # Increment the flag
        flash(f'{flag} ARP IPs Deleted Successfully', 'success')  # Flash a success message
        functions.create_log(session['user_id'], f'{flag} ARP IPs Deleted', 'DELETE', 'router_scan')  # Create a log
        return jsonify({'message': 'ARP IPs deleted successfully'}), 200  # Return a success message
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return jsonify({'message': 'Failed to delete ARP IPs', 'error': str(e)}), 500
# Scan Bulk Delete Route

# Scan Delete All Route
@scan_bp.route('/delete/all', methods=['POST'])
@restriction.login_required  # Need to be logged in
@restriction.admin_required  # Need to be an admin
def delete_all_arps_ips():
    try:  # Try to delete all ARP IPs
        ARPTags.delete_all_arp_tags()  # Delete all ARP Tags
        ARP.delete_all_arps()  # Delete all ARP IPs
        functions.create_log(session['user_id'], 'All ARP IPs Deleted', 'DELETE', 'router_scan')  # Create a log
        flash('All ARP IPs Deleted Successfully', 'success')  # Flash a success message
        return jsonify({'message': 'All ARP IPs deleted successfully'}), 200  # Return a success message
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return jsonify({'message': 'Failed to delete ARP IPs', 'error': str(e)}), 500
# Scan Delete All Route

# Scan Get Scan Details Route
@scan_bp.route('/get_scan_details/', methods=['GET'])
def get_scan_details():
    try:  # Try to get the ARP details
        arp_id = request.args.get('id')  # Get the ARP ID
        arp_item = ARP.get_arp(arp_id)  # Get the ARP Item
        arp_tags = ARPTags.get_arp_tags(arp_id)  # Get the ARP Tags
        segment = str(IPSegment.query.get(arp_item.fk_ip_address_id).ip_segment_ip + "/" + IPSegment.query.get(
            arp_item.fk_ip_address_id).ip_segment_mask)  # Get the segment
        return jsonify([{  # Return the ARP details
            'id': ["Identifier", arp_item.arp_id],  # ID
            'segment': ["IP Segment", segment],  # Segment
            'ip': ["ARP IP", arp_item.arp_ip],  # IP
            'mac': ["ARP MAC", arp_item.arp_mac],  # MAC
            'alias': ["ARP Alias", arp_item.arp_alias],  # Alias
            'tags': arp_tags,  # Tags
            'arp_interface': ["ARP Interface", arp_item.arp_interface],  # Interface
            'arp_is_dhcp': ["ARP is DHCP?", arp_item.arp_is_dhcp],  # DHCP
            'arp_is_invalid': ["ARP is Invalid?", arp_item.arp_is_invalid],  # Invalid
            'arp_is_dynamic': ["ARP is Dynamic?", arp_item.arp_is_dynamic],  # Dynamic
            'arp_is_complete': ["ARP is Complete?", arp_item.arp_is_complete],  # Complete
            'arp_is_disabled': ["ARP is Disabled?", arp_item.arp_is_disabled],  # Disabled
            'arp_is_published': ["ARP is Published?", arp_item.arp_is_published],  # Published
        }]), 200  # Return a success message
    except Exception as e:  # If an exception occurs
        return jsonify({'message': 'Failed to get ARP details', 'error': str(e)}), 500  # Return an error message
# Scan Get Scan Details Route

# Socket IO Sockets
# ARP Scan Process Sockets
# Start ARP Scan Process Socket
@socketio.on('start_arp_scan')
def handle_start_progress():
    min_duration = 3  # Duration in seconds

    start_time = time.time()  # Start time of the process
    RouterAPI.arp_scan()  # Start the ARP router_scan process
    end_time = time.time()  # End time of the process

    actual_duration = end_time - start_time  # Actual duration of the process
    total_duration = max(min_duration, int(actual_duration))  # Ensure that the duration is at least min_duration

    eventlet.sleep(total_duration)  # Sleep for the total duration

    socketio.emit('finish_arp_scan')  # Emit the finish_arp_scan event
# Start ARP Scan Process Socket
# ARP Scan Process Routes
# Socket IO Routes
