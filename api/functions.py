class APIFunctions:

    def __init__(self) -> None:
        pass

    @staticmethod
    def verify_user_existence(user_id: int) -> None:
        from models.users.models import User
        from utils.threading_manager import ThreadingManager
        try:
            return ThreadingManager().run_thread(User.verify_user_identifier, 'rx', user_id)
        except Exception as e:
            raise e

    @staticmethod
    def create_transaction_log(user_id: int, description: str, action: str, table: str, public: str,
                               local: str = '') -> None:
        from datetime import datetime
        from entities.user_log import UserLogEntity
        from models.users.models import User, UserLog
        from utils.threading_manager import ThreadingManager

        try:
            user = ThreadingManager().run_thread(User.get_user, 'rx', user_id)

            user_log = UserLogEntity(
                user_log_id=int(),
                rk_user_id=int(user.user_id),
                rk_user_username=str(user.user_username),
                rk_user_name=str(user.user_name),
                rk_user_lastname=str(user.user_lastname),
                user_log_description=str(description),
                user_log_action=str(action),
                user_log_table=str(table),
                user_log_date=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                user_log_public_ip=str(public),
                user_log_local_ip=str(local)
            )

            user_log.validate()
            ThreadingManager().run_thread(UserLog.add_user_log, 'w', user_log)
        except Exception as e:
            raise e
