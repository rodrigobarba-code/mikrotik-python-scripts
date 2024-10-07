# Import this module to start the FastAPI server using Hypercorn
import subprocess
from threading import Thread

# Function to start the FastAPI server using Hypercorn
def start_hypercorn():
    command = [
        "hypercorn",
        "api:fastapi_app",
        "--bind", "0.0.0.0:8080",
        "--workers", "6",
        "--reload"
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while starting Hypercorn: {e}")

# Function to start the FastAPI server in a separate thread
def start():
    hypercorn_thread = Thread(target=start_hypercorn)
    hypercorn_thread.start()
    hypercorn_thread.join()
