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

# Start the FastAPI server using Hypercorn in a separate thread
if __name__ == "__main__":
    thread = Thread(target=start_hypercorn)
    thread.start()
    thread.join()
