# Importing necessary modules
import eventlet
from flask_socketio import emit, SocketIO
from flask import render_template, session
# Importing necessary modules

# Importing necessary decorators
# Importing necessary decorators

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

    while progress < 100:  # Looping until the progress reaches 100
        eventlet.sleep(1)  # Sleeping for 1 second
        progress += 5  # Incrementing the progress by 5
        progress_data['progress'] = progress  # Setting the progress data
        emit(  # Emitting the progress update
            'arp_scan_process_update',  # Event name
            {'progress': progress}, broadcast=True  # Data and broadcasting the event
        )

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
