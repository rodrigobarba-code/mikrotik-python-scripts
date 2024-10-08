import threading
from start_app import start_flask
from start_api import start_hypercorn

# Run the init functions
if __name__ == '__main__':
    # Start the Flask app
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

    # Start the Hypercorn server
    hypercorn_thread = threading.Thread(target=start_hypercorn)
    hypercorn_thread.start()

    # Wait for the threads to finish
    flask_thread.join()
    hypercorn_thread.join()
