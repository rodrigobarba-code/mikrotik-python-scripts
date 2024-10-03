from app import create_app
from threading import Thread
from websockets import socketio
from app.config import AppConfig, UserJobs, Sidebar

flask_app = create_app()

@flask_app.context_processor
def injects():
    return dict(
        metadata=AppConfig.METADATA,
        menu_items=Sidebar.menu_items,
        job_display=UserJobs.job_display,
        profile_menu_items=Sidebar.profile_menu_items
    )

def start_flask():
    socketio.run(flask_app,
                 host="0.0.0.0", port=AppConfig.PORT,
                 debug=AppConfig.DEBUG, use_reloader=False,
                 allow_unsafe_werkzeug=True)

def start_hypercorn():
    import subprocess

    command = [
        "hypercorn",
        "api:fastapi_app",
        "--bind", "0.0.0.0:8080",
        "--workers", "4",
        "--reload"
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while starting Hypercorn: {e}")

if __name__ == "__main__":
    hypercorn_thread = Thread(target=start_hypercorn)
    flask_thread = Thread(target=start_flask)

    hypercorn_thread.start()
    flask_thread.start()

    hypercorn_thread.join()
    flask_thread.join()
