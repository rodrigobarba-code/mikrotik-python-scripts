"""
# Version: 1.0
This file contains the events that are emitted by the socketio server
and the functions that handle the events.

Events:
    - init_scan: Event to initialize the scan process
    - start_scan: Event to start the scan process
    - get_general_status: Event to get the general status of the scan process
    - return_to_router_scan: Event to return to the router scan page
"""

# Import the necessary modules
import asyncio
from time import sleep
from api.routeros.api import RouterAPI
from websockets.socketio_manager import SocketIOManager

# Define the scan_process function to initialize the events
def scan_process(socketio) -> None:
    # Event to connect to the socketio server
    socketio.emit('connect')

    # Event to initialize the scan process
    @socketio.on('init_scan')
    def scan_routeros() -> None:
        """
        Function to initialize the scan process
        :return: None
        """

        # Set the scan status to 1, or in progress
        SocketIOManager.set_scan_status(1)

        # Emit the redirect_to_loading event to redirect to the loading page
        socketio.emit(
            'redirect_to_loading',
            {
                'url': '/router/scan/loading',
                'action': 'start_scan'
            }
        )

    # Event to start the scan process
    @socketio.on('start_scan')
    def start_scan_routeros() -> None:
        """
        Function to start the scan process
        :return: None
        """

        # Set the scan status to 2, or scanning
        asyncio.run(RouterAPI.arp_scan())

    @socketio.on('error_on_scan')
    def error_on_scan_routeros() -> None:
        """
        Function to emit an error event
        :return: None
        """

        # Emit the error event to show an error message
        socketio.emit(
            'error',
            {
                'url': '/router/scan',
            }
        )

    # Event to get the general status of the scan process
    @socketio.on('get_general_status')
    def scan_status_routeros() -> None:
        """
        Function to get the general status of the scan process
        :return: None
        """

        # Get the percentage of the scan process and the message
        percent = SocketIOManager.get_percent()
        message = SocketIOManager.get_message()

        # Get the status of the scan process
        status = SocketIOManager.get_scan_status()

        # Emit the status event to update the status of the scan process
        socketio.emit(
            'status',
            {
                'scan_status': message,
                'percent': percent,
                'status': status
            }
        )

    # Event to return to the router scan page
    @socketio.on('return_to_router_scan')
    def return_to_router_scan() -> None:
        """
        Function to return to the router scan page
        :return: None
        """

        try:
            # Emit the scan_status event to update the scan status
            socketio.emit(
                'scan_status',
                {
                    'scan_status': 'Scan Completed, redirecting to scan page',
                    'percentage': 100
                }
            )

            sleep(5) # Sleep for 5 seconds

            # Emit the redirect_to_router_scan event to redirect to the router scan page
            socketio.emit(
                'redirect_to_router_scan',
                {
                    'url': '/router/scan',
                    'action': 'return_to_scan'
                }
            )
        except Exception as e:
            print(e)
