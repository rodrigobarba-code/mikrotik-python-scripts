"""
# Version: 1.0
This module is used to manage the socketio instance and the message and percent variables
    Attributes:
        _message (str): The message that will be displayed in the frontend
        _percent (int): The percentage of the scan
        _instance (SocketIO): The instance of the socketio

    Methods:
        get_instance(): Returns the instance of the socketio
        get_message(): Returns the message
        set_message(): Sets the message
        get_percent(): Returns the percentage
        set_percent(): Sets the percentage
        get_scan_status(): Returns the scan status
        set_scan_status(): Sets the scan status
"""

# Importing the necessary libraries
from flask_socketio import SocketIO

# SocketIOManager Class
class SocketIOManager:
    _message: str = 'Scan in Progress...'  # Default Message
    _percent: int = 0  # Default Percentage
    _instance = None  # Default Instance
    _scan_status: int = 0  # Default Scan Status

    # Constructor
    def __init__(self):
        """
        This method initializes the socketio instance
        :return: None
        """

        # If the instance is not created, create the instance
        if not SocketIOManager._instance:
            SocketIOManager._instance = SocketIO()

    # Static Method to get the instance
    @staticmethod
    def get_instance():
        """
        This method returns the instance of the socketio
        :return: SocketIO Instance
        """

        # If the instance is not created, create the instance
        if not SocketIOManager._instance:
            SocketIOManager()

        # Return the instance
        return SocketIOManager._instance

    # Static Method to get the message
    @staticmethod
    def get_message():
        """
        This method returns the message
        :return: str
        """
        return SocketIOManager._message

    # Static Method to set the message
    @staticmethod
    def set_message(message):
        """
        This method sets the message
        :param message: str
        :return: None
        """
        SocketIOManager._message = message

    # Static Method to get the percentage
    @staticmethod
    def get_percent():
        """
        This method returns the percentage
        :return: int
        """
        return SocketIOManager._percent

    # Static Method to set the percentage
    @staticmethod
    def set_percent(percent):
        """
        This method sets the percentage
        :param percent: int
        :return: None
        """
        SocketIOManager._percent = percent

    # Static Method to get the scan status
    @staticmethod
    def get_scan_status():
        """
        This method returns the scan status
        :return: int
        """
        return SocketIOManager._scan_status

    # Static Method to set the scan status
    @staticmethod
    def set_scan_status(scan_status):
        """
        This method sets the scan status
        :param scan_status: int
        :return: None
        """
        SocketIOManager._scan_status = scan_status
