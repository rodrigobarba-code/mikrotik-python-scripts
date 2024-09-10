from app import create_app
from threading import Thread
from websockets import socketio

from app.config import AppConfig, UserJobs, Sidebar

flask_app = create_app()

@flask_app.context_processor
def injects():
    return dict(
        metadata=AppConfig.METADATA, menu_items=Sidebar.menu_items,
        job_display=UserJobs.job_display, profile_menu_items=Sidebar.profile_menu_items)

def start_flask():
    socketio.run(flask_app,
                 host="0.0.0.0", port=AppConfig.PORT,
                 debug=AppConfig.DEBUG, use_reloader=False,
                 allow_unsafe_werkzeug=True)

if __name__ == "__main__":
    flask_thread = Thread(target=start_flask)
    flask_thread.start()
    flask_thread.join()
