import os
import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class ThreadingManager:
    user = os.environ.get('DB_USER', 'sevensuiteuser')
    password = os.environ.get('DB_PASSWORD', 'development-sevensuiteapp')
    host = os.environ.get('DB_HOST', 'localhost:3306')  # For Development
    # host = os.environ.get('DB_HOST', 'mariadb-database:3306')  # For Docker
    database = os.environ.get('DB_NAME', 'sevensuite')

    connection_string = f'mariadb+mariadbconnector://{user}:{password}@{host}/{database}'
    DB_URI = connection_string

    def __init__(self):
        self.engine = create_engine(self.DB_URI)
        self.Session = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)

    def run_thread(self, func, type, object=None):
        result = [None]
        error = [None]

        def target_func():
            try:
                self._execute(func, type, object, result)
            except Exception as e:
                error[0] = e

        thread = threading.Thread(target=target_func)
        thread.start()
        thread.join()

        if error[0] is not None:
            raise error[0]

        return result[0]

    def _execute(self, func, type, object, result):
        session = self.Session()
        try:
            print(f"{'Writing' if type in ['w', 'wx'] else 'Reading'} Thread: {func.__name__} Running")

            if type in ['r', 'rx', 'rxc']:
                result[0] = func(session, object) if type in ['rx', 'rxc'] else func(session)
                if type == 'rxc':
                    session.commit()
                    session.close()
            elif type in ['w', 'wx']:
                func(session, object) if type == 'w' else func(session)
                session.commit()
                session.close()
        except Exception as e:
            print(f"{'Writing' if type in ['w', 'wx'] else 'Reading'} Thread: {e} Error")
            session.rollback()
            session.close()
            raise e
