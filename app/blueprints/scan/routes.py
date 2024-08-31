# Importing necessary modules
import time
import eventlet
from flask import render_template
from flask_socketio import SocketIO
# Importing necessary modules

# Importing Router API
from app.api.api import RouterAPI
# Importing Router API

# Importing necessary models
from app.blueprints.scan.models import ARP, ARPTags
from app.blueprints.ip_addresses.models import IPSegment
# Importing necessary models

# Importing necessary entities
from app.blueprints.scan.entities import ARPTag, ARPEntity
# Importing necessary entities

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
    total_duration = max(min_duration, actual_duration)  # Ensure that the duration is at least min_duration

    eventlet.sleep(total_duration)  # Sleep for the total duration

    socketio.emit('finish_arp_scan')  # Emit the finish_arp_scan event
# Start ARP Scan Process Socket
# ARP Scan Process Routes
# Socket IO Routes
