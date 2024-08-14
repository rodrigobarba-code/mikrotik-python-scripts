# Importing necessary modules
import eventlet
from flask_socketio import emit, SocketIO
from flask import render_template, session
# Importing necessary modules

# Importing necessary decorators
# Importing necessary decorators

from . import scan_bp  # Importing the blueprint instance

progress_data = {}  # Initializing the progress data
socketio = SocketIO()  # Initializing the socketio instance

# Scan Main Route
@scan_bp.route('/scan', methods=['GET', 'POST'])
def scan():
    return render_template('scan/scan.html')
# Scan Main Route

# SocketIO Routes
@socketio.on('start_progress')
def handle_start_progress():
    user_id = session.get('user_id')
    progress = 0
    progress_data[user_id] = progress

    while progress < 100:
        eventlet.sleep(1)
        progress += 5
        progress_data[user_id] = progress
        emit('progress_update', {'progress': progress}, broadcast=True)

    emit('progress_complete', broadcast=True)

@socketio.on('get_progress')
def handle_get_progress():
    user_id = session.get('user_id')
    progress = progress_data.get(user_id, 0)
    emit('progress_update', {'progress': progress})
# SocketIO Routes
