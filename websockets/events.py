from flask_socketio import emit

def register_handlers(socketio):
    # Handle connection event
    @socketio.on('connect')
    def handle_connect():
        print("Client connected")
        emit('response', {'message': 'Connected successfully'})

    # Handle disconnection event
    @socketio.on('disconnect')
    def handle_disconnect():
        print("Client disconnected")

    # Custom event example
    @socketio.on('my_event')
    def handle_my_event(data):
        print(f"Received event: {data}")
        emit('response', {'message': 'Event received'})
