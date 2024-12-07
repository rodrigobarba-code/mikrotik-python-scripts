import bcrypt
from .. import Base
from dateutil import parser
from datetime import datetime
from entities.user import UserEntity
from entities.user_log import UserLogEntity
from sqlalchemy import Column, Integer, String, text
from models.users.functions import UsersFunctions


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_username = Column(String(128), nullable=False)
    user_email = Column(String(128), nullable=True)
    user_password = Column(String(128), nullable=False)
    user_name = Column(String(128), nullable=False)
    user_lastname = Column(String(128), nullable=False)
    user_privileges = Column(String(128), nullable=False)
    user_state = Column(Integer, default=1, nullable=False)

    def __repr__(self):
        return f'<User {self.user_id}>'

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_username': self.user_username,
            'user_email': self.user_email,
            'user_password': self.user_password,
            'user_name': self.user_name,
            'user_lastname': self.user_lastname,
            'user_privileges': self.user_privileges,
            'user_state': self.user_state
        }

    @staticmethod
    def verify_autoincrement_id(session):
        try:
            if not session.query(User).all():
                session.execute(text("ALTER TABLE users AUTO_INCREMENT = 1"))
        except Exception as e:
            raise e

    @staticmethod
    def add_user(session, user: UserEntity):
        model_u = User
        v_user = UsersFunctions()
        try:
            if v_user.validate_user(session, user, "insert", model_u):
                hashed_password = bcrypt.hashpw(user.user_password.encode('utf-8'), bcrypt.gensalt())
                new_user = User(
                    user_id=0,
                    user_username=str(user.user_username),
                    user_email=str(user.user_email),
                    user_password=hashed_password,
                    user_name=str(user.user_name),
                    user_lastname=str(user.user_lastname),
                    user_privileges=str(user.user_privileges),
                    user_state=int(user.user_state)
                )
                session.add(new_user)
            else:
                raise Exception()
        except Exception as e:
            raise e

    @staticmethod
    def update_user(session, new_user: UserEntity):
        try:
            model_u = User
            v_user = UsersFunctions()
            if v_user.validate_user(session, new_user, "update", model_u):
                hashed_password = bcrypt.hashpw(new_user.user_password.encode('utf-8'), bcrypt.gensalt())
                old_user = session.query(User).get(new_user.user_id)
                old_user.user_username = new_user.user_username
                if new_user.user_email != old_user.user_email:
                    old_user.user_email = new_user.user_email
                if new_user.user_password != old_user.user_password and new_user.user_password != '':
                    old_user.user_password = hashed_password
                old_user.user_name = new_user.user_name
                old_user.user_lastname = new_user.user_lastname
                old_user.user_privileges = new_user.user_privileges
                old_user.user_state = new_user.user_state
            else:
                raise Exception()
        except Exception as e:
            raise e

    @staticmethod
    def update_settings_user(session, new_user: UserEntity):
        try:
            model_u = User
            v_user = UsersFunctions()
            if v_user.validate_user(session, new_user, "update", model_u):
                old_user = session.query(User).get(new_user.user_id)
                old_user.user_username = new_user.user_username
                old_user.user_name = new_user.user_name
                old_user.user_lastname = new_user.user_lastname
            else:
                raise Exception()
        except Exception as e:
            raise e

    @staticmethod
    def update_password(session, new_user: UserEntity):
        try:
            model_u = User
            v_user = UsersFunctions()
            if v_user.validate_user(session, new_user, "update", model_u):
                hashed_password = bcrypt.hashpw(new_user.user_password.encode('utf-8'), bcrypt.gensalt())
                old_user = session.query(User).get(new_user.user_id)
                old_user.user_password = hashed_password
            else:
                raise Exception()
        except Exception as e:
            raise e

    @staticmethod
    def delete_user(session, user_id: int):
        model_u = User
        v_user = UsersFunctions()
        try:
            if v_user.validate_user(
                    session,
                    UserEntity(
                        user_id=user_id,
                        user_username=str(),
                        user_email=str(),
                        user_password=str(),
                        user_name=str(),
                        user_lastname=str(),
                        user_privileges=str(),
                        user_state=int()
                    ),
                    "delete",
                    model_u
            ):
                user = session.query(User).get(user_id)
                session.delete(user)
            else:
                raise Exception()
        except Exception as e:
            raise e

    @staticmethod
    def bulk_delete_users(session, user_ids):
        model_u = User
        v_user = UsersFunctions()
        try:
            if v_user.validate_bulk_delete(session, model_u, user_ids):
                for user_id in user_ids:
                    user = session.query(User).get(user_id)
                    session.delete(user)
            else:
                raise Exception()
        except Exception as e:
            raise

    @staticmethod
    def delete_all_users(session):
        try:
            session.query(User).delete()
        except Exception as e:
            raise e

    @staticmethod
    def get_user(session, user_id: int):
        model_u = User
        v_user = UsersFunctions()
        try:
            if v_user.validate_user(
                    session,
                    UserEntity(
                        user_id=user_id,
                        user_username=str(),
                        user_email=str(),
                        user_password=str(),
                        user_name=str(),
                        user_lastname=str(),
                        user_privileges=str(),
                        user_state=int()
                    ),
                    "get",
                    model_u
            ):
                user = session.query(User).get(user_id)
                obj = UserEntity(
                    user_id=user.user_id,
                    user_username=user.user_username,
                    user_email=user.user_email,
                    user_password=str(),
                    user_name=user.user_name,
                    user_lastname=user.user_lastname,
                    user_privileges=user.user_privileges,
                    user_state=user.user_state
                )
                obj.validate()
                return obj
            else:
                raise Exception()
        except Exception as e:
            raise e

    @staticmethod
    def get_user_by_username(session, user_username: str):
        try:
            user = session.query(User).filter(User.user_username == user_username).first()
            if user is None:
                return None
            obj = UserEntity(
                user_id=user.user_id,
                user_username=user.user_username,
                user_email=user.user_email,
                user_password=str(),
                user_name=user.user_name,
                user_lastname=user.user_lastname,
                user_privileges=user.user_privileges,
                user_state=user.user_state
            )
            obj.validate()
            return obj
        except Exception as e:
            raise e

    @staticmethod
    def get_users(session):
        try:
            r_list = []
            users = session.query(User).all()
            for user in users:
                obj = UserEntity(
                    user_id=user.user_id,
                    user_username=user.user_username,
                    user_email=user.user_email,
                    user_password=str(),
                    user_name=user.user_name,
                    user_lastname=user.user_lastname,
                    user_privileges=user.user_privileges,
                    user_state=user.user_state
                )
                obj.validate()
                r_list.append(obj)
            return r_list
        except Exception as e:
            raise e

    @staticmethod
    def verify_user_identifier(session, user_id: int) -> bool:
        try:
            user = session.query(User).get(user_id)
            if user is None:
                return False
            return True
        except Exception as e:
            raise e

    @staticmethod
    def validate_credentials(session, credentials: dict) -> dict:
        try:
            user_db = session.query(User).filter(User.user_username == credentials['user_username']).first()

            if user_db is None:
                return {
                    'authenticated': False
                }

            hashed_password = user_db.user_password.encode('utf-8') if isinstance(user_db.user_password,
                                                                                  str) else user_db.user_password
            authenticated = bcrypt.checkpw(credentials['user_password'].encode('utf-8'), hashed_password)

            if authenticated:
                return {
                    'user_id': int(user_db.user_id),
                    'authenticated': authenticated,
                }

            return {
                'authenticated': authenticated,
            }
        except Exception as e:
            return e

    @staticmethod
    def reset_password_with_random(session, user_email: str) -> dict:
        """
        Reset the password of a user with a random password.
        :param session: SQLAlchemy session
        :param user_email: Email of the user
        :return: New password
        """
        try:
            # Import the necessary modules
            import random
            import string

            # Create a random password
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            # Hash the password
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

            # Get the user using email
            user = session.query(User).filter(User.user_email == user_email).first()

            # Verify if the user exists
            if user is None:
                raise Exception(f"User with email '{user_email}' not found.")
            if user.user_state == 0:
                raise Exception(f"Your account is disabled. Please contact the administrator.")

            # Update the user password
            user.user_password = hashed_password

            # Return the new password
            return {
                'user_name': user.user_name,
                'user_lastname': user.user_lastname,
                'new_password': new_password
            }
        except Exception as e:
            raise e


class UserLog(Base):
    __tablename__ = 'users_log'

    user_log_id = Column(Integer, primary_key=True, autoincrement=True)
    rk_user_id = Column(Integer, nullable=False)
    rk_user_username = Column(String(128), nullable=False)
    rk_user_name = Column(String(128), nullable=False)
    rk_user_lastname = Column(String(128), nullable=False)
    user_log_description = Column(String(256), nullable=True)
    user_log_action = Column(String(128), nullable=False)
    user_log_table = Column(String(128), nullable=True)
    user_log_date = Column(String(128), nullable=False)
    user_log_public_ip = Column(String(32), nullable=False)
    user_log_local_ip = Column(String(32), nullable=False)

    def __repr__(self):
        return f'<UserLog {self.user_log_id}>'

    def to_dict(self):
        return {
            'user_log_id': self.user_log_id,
            'rk_user_id': self.rk_user_id,
            'rk_user_username': self.rk_user_username,
            'rk_user_name': self.rk_user_name,
            'rk_user_lastname': self.rk_user_lastname,
            'user_log_description': self.user_log_description,
            'user_log_action': self.user_log_action,
            'user_log_table': self.user_log_table,
            'user_log_date': self.user_log_date,
            'user_log_public_ip': self.user_log_public_ip,
            'user_log_local_ip': self.user_log_local_ip
        }

    @staticmethod
    def verify_autoincrement_id(session):
        try:
            if not session.query(UserLog).all():
                session.execute(text("ALTER TABLE users_log AUTO_INCREMENT = 1"))
        except Exception as e:
            raise e

    @staticmethod
    def add_user_log(session, user_log: UserLogEntity):
        from models.users.exceptions import UserLogDatabaseError
        try:
            new_user_log = UserLog(
                user_log_id=None,
                rk_user_id=user_log.rk_user_id,
                rk_user_username=user_log.rk_user_username,
                rk_user_name=user_log.rk_user_name,
                rk_user_lastname=user_log.rk_user_lastname,
                user_log_description=user_log.user_log_description,
                user_log_action=user_log.user_log_action,
                user_log_table=user_log.user_log_table,
                user_log_date=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                user_log_public_ip=user_log.user_log_public_ip,
                user_log_local_ip=user_log.user_log_local_ip
            )
            session.add(new_user_log)
            return user_log
        except Exception as e:
            raise UserLogDatabaseError()

    @staticmethod
    def delete_from_date_user_log(session, date_str):
        try:
            flag = 0
            date_tmp = parser.parse(date_str)
            from_date = datetime(date_tmp.year, date_tmp.month, date_tmp.day, date_tmp.hour, date_tmp.minute,
                                 date_tmp.second)

            for user_log in session.query(UserLog).all():
                user_log_date = datetime.strptime(user_log.user_log_date, '%d/%m/%Y %H:%M:%S')

                if user_log_date <= from_date:
                    session.delete(user_log)
                    flag += 1

            return flag
        except Exception as e:
            raise e

    @staticmethod
    def delete_all_user_log(session):
        from models.users.exceptions import UserLogDatabaseError
        try:
            session.query(UserLog).delete()
        except Exception as e:
            raise UserLogDatabaseError()

    @staticmethod
    def get_user_logs(session):
        from models.users.exceptions import UserLogError
        try:
            r_list = []
            user_logs = session.query(UserLog).order_by(UserLog.user_log_date.desc()).all()
            for user_log in user_logs:
                obj = UserLogEntity(
                    user_log_id=user_log.user_log_id,
                    rk_user_id=user_log.rk_user_id,
                    rk_user_username=user_log.rk_user_username,
                    rk_user_name=user_log.rk_user_name,
                    rk_user_lastname=user_log.rk_user_lastname,
                    user_log_description=user_log.user_log_description,
                    user_log_action=user_log.user_log_action,
                    user_log_table=user_log.user_log_table,
                    user_log_date=user_log.user_log_date,
                    user_log_public_ip=user_log.user_log_public_ip,
                    user_log_local_ip=user_log.user_log_local_ip
                )
                obj.validate()
                r_list.append(obj)
            return r_list
        except Exception as e:
            raise UserLogError()
