from start_api import start as api_start  # Import the start function from start_api.py
from start_app import start as app_start  # Import the start function from start_app.py

# Run the init functions
if __name__ == '__main__':
    api_start()
    app_start()
