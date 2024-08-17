# Importing necessary modules
import time
import eventlet
from flask import render_template
from flask_socketio import SocketIO, emit
# Importing necessary modules

# Importing Router API
from app.api.api import RouterAPI
# Importing Router API

from . import scan_bp  # Importing the blueprint instance

progress_data = {
    'progress': 0  # Initializing the progress data
}

socketio = SocketIO()  # Initializing the socketio instance

# Scan Main Route
@scan_bp.route('/scan', methods=['GET', 'POST'])
def scan():
    return render_template('scan/scan.html')  # Rendering Router Scan Template
# Scan Main Route

# Socket IO Sockets
# ARP Scan Process Sockets
# Start ARP Scan Process Socket
@socketio.on('start_arp_scan_process')
def start_arp_scan_process():
    progress = 0  # Initializing the progress
    progress_data['progress'] = progress  # Setting the progress data
    try:
        start_time = time.time()  # Getting the start time
        RouterAPI.scan_arp()  # Scanning the ARP
        end_time = time.time()  # Getting the end time
        duration = end_time - start_time  # Calculating the duration
        for i in range(100):
            progress = duration * i / 100  # Calculating the progress
            progress_data['progress'] = progress
            emit(  # Emitting the progress update
                'arp_scan_process_update',  # Event name
                {'progress': progress}  # Data
            )
            eventlet.sleep(0.1)  # Sleeping for 0.1 seconds
    except Exception as e:  # If an exception occurs
        print(str(e))
    emit(  # Emitting the progress complete
        'arp_scan_process_complete',  # Event name
        broadcast=True  # Broadcasting the event
    )
# Start ARP Scan Process Socket

# Get ARP Scan Progress Socket
@socketio.on('get_arp_scan_progress')
def get_arp_scan_progress():
    progress = progress_data['progress']  # Getting the progress data
    emit(  # Emitting the progress update
        'arp_scan_process_update',   # Event name
        {'progress': progress}  # Data
    )
# Get ARP Scan Progress Socket
# ARP Scan Process Routes
# Socket IO Routes
