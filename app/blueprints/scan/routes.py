# Description: Scanning Routes for the Scan Blueprint

# Importing necessary modules
import time
import eventlet
from flask_socketio import SocketIO
from flask import render_template, request, redirect, url_for, flash, session, jsonify
# Importing necessary modules

# Importing Required Local Modules
from app.blueprints.users.functions import users_functions as functions  # Import the users functions object
# Importing Required Local Modules

# Importing Router API
from app.api.api import RouterAPI
# Importing Router API

# Importing Required Decorators
from app.decorators import RequirementsDecorators as restriction
# Importing Required Decorators

# Importing necessary entities

# Importing necessary entities

# Importing necessary models
from app.blueprints.scan.models import ARP, ARPTags
from app.blueprints.ip_addresses.models import IPSegment
# Importing necessary models

from . import scan_bp  # Importing the blueprint instance

socketio = SocketIO()  # Initializing the socketio instance

# Scan Main Route
@scan_bp.route('/scan', methods=['GET', 'POST'])
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
        'scan/scan.html',  # Rendering the scan template
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
        functions.create_log(session['user_id'], 'ARP IP Deleted', 'DELETE', 'scan')  # Create a log
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
    return redirect(url_for('scan.scan'))  # Redirect to the scan route
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
        functions.create_log(session['user_id'], f'{flag} ARP IPs Deleted', 'DELETE', 'scan')  # Create a log
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
        functions.create_log(session['user_id'], 'All ARP IPs Deleted', 'DELETE', 'scan')  # Create a log
        flash('All ARP IPs Deleted Successfully', 'success')  # Flash a success message
        return jsonify({'message': 'All ARP IPs deleted successfully'}), 200  # Return a success message
    except Exception as e:  # If an exception occurs
        flash(str(e), 'danger')  # Flash an error message
        return jsonify({'message': 'Failed to delete ARP IPs', 'error': str(e)}), 500
# Scan Delete All Route

# Socket IO Sockets
# ARP Scan Process Sockets
# Start ARP Scan Process Socket
@socketio.on('start_arp_scan')
def handle_start_progress():
    min_duration = 3  # Duration in seconds

    start_time = time.time()  # Start time of the process
    RouterAPI.arp_scan()  # Start the ARP scan process
    end_time = time.time()  # End time of the process

    actual_duration = end_time - start_time  # Actual duration of the process
    total_duration = max(min_duration, int(actual_duration))  # Ensure that the duration is at least min_duration

    eventlet.sleep(total_duration)  # Sleep for the total duration

    socketio.emit('finish_arp_scan')  # Emit the finish_arp_scan event
# Start ARP Scan Process Socket
# ARP Scan Process Routes
# Socket IO Routes
