from flask_socketio import SocketIO

class SocketIOManager:
    _message: str = None
    _percent: int = None
    _instance = None
    _scan_status: int = None

    def __init__(self):
        if not SocketIOManager._instance:
            SocketIOManager._instance = SocketIO()

    @staticmethod
    def get_instance():
        if not SocketIOManager._instance:
            SocketIOManager()
        return SocketIOManager._instance

    @staticmethod
    def get_message():
        return SocketIOManager._message

    @staticmethod
    def set_message(message):
        SocketIOManager._message = message

    @staticmethod
    def get_percent():
        return SocketIOManager._percent

    @staticmethod
    def set_percent(percent):
        SocketIOManager._percent = percent

    @staticmethod
    def get_scan_status():
        return SocketIOManager._scan_status

    @staticmethod
    def set_scan_status(scan_status):
        SocketIOManager._scan_status = scan_status
