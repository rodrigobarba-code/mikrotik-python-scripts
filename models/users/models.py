import bcrypt
from datetime import datetime
from .. import Base, SessionLocal
from sqlalchemy import Column, Integer, String

from entities.user import UserEntity
from entities.user_log import UserLogEntity

from models.users.functions import UsersFunctions

class User(Base):
    __tablename__ = 'users'  

    user_id = Column(Integer, primary_key=True, autoincrement=True)  
    user_username = Column(String(128), nullable=False)  
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
            'user_password': self.user_password,  
            'user_name': self.user_name,  
            'user_lastname': self.user_lastname,  
            'user_privileges': self.user_privileges,  
            'user_state': self.user_state  
        }

    @staticmethod
    def add_user(user: UserEntity):
        model_u = User
        session = SessionLocal()
        v_user = UsersFunctions()  
        try:
            if v_user.validate_user(user, "insert", model_u):
                hashed_password = bcrypt.hashpw(user.user_password.encode('utf-8'), bcrypt.gensalt())
                new_user = User(  
                    user_id=None,  
                    user_username=str(user.user_username),  
                    user_password=hashed_password,  
                    user_name=str(user.user_name),  
                    user_lastname=str(user.user_lastname),  
                    user_privileges=str(user.user_privileges),  
                    user_state=str(user.user_state)  
                )
                session.add(new_user)  
                session.commit()
            else:  
                raise Exception()  
        except Exception as e:  
            session.rollback()  
            raise e  

    @staticmethod
    def update_user(new_user: UserEntity):
        session = SessionLocal()
        try:
            model_u = User  
            v_user = UsersFunctions()
            if v_user.validate_user(new_user, "update", model_u):
                hashed_password = bcrypt.hashpw(new_user.user_password.encode('utf-8'), bcrypt.gensalt())  
                old_user = User.query.get(new_user.user_id)  
                old_user.user_username = new_user.user_username  
                if new_user.user_password != old_user.user_password and new_user.user_password != '':  
                    old_user.user_password = hashed_password  
                old_user.user_name = new_user.user_name  
                old_user.user_lastname = new_user.user_lastname  
                old_user.user_privileges = new_user.user_privileges  
                old_user.user_state = new_user.user_state  
                session.commit()  
            else:  
                raise Exception()  
        except Exception as e:  
            session.rollback()  
            raise e  

    @staticmethod
    def delete_user(user_id: int):
        model_u = User
        session = SessionLocal()
        v_user = UsersFunctions()  
        try:
            if v_user.validate_user(
                    UserEntity(
                        user_id=user_id,  
                        user_username=str(),  
                        user_password=str(),  
                        user_name=str(),  
                        user_lastname=str(),  
                        user_privileges=str(),  
                        user_state=int()  
                    ),
                    "delete",  
                    model_u  
            ):
                user = User.query.get(user_id)
                session.delete(user)  
                session.commit()  
            else:  
                raise Exception()  
        except Exception as e:  
            session.rollback()  
            raise e  

    @staticmethod
    def delete_all_users():
        session = SessionLocal()
        try:
            User.query.delete()  
            session.commit()  
        except Exception as e:  
            session.rollback()  
            raise e
    
    @staticmethod
    def get_user(user_id: int):
        model_u = User  
        v_user = UsersFunctions()  
        try:
            if v_user.validate_user(
                    UserEntity(
                        user_id=user_id,  
                        user_username=str(),  
                        user_password=str(),  
                        user_name=str(),  
                        user_lastname=str(),  
                        user_privileges=str(),  
                        user_state=int()  
                    ),
                    "get",  
                    model_u  
            ):
                user = User.query.get(user_id)
                obj = UserEntity(  
                    user_id=user.user_id,  
                    user_username=user.user_username,  
                    user_password=bcrypt.hashpw(user.user_password, bcrypt.gensalt()).decode('utf-8'),  
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
    def get_users():
        try:
            r_list = []  
            users = User.query.all()  
            for user in users:  
                obj = UserEntity(  
                    user_id=user.user_id,  
                    user_username=user.user_username,  
                    user_password=bcrypt.hashpw(user.user_password, bcrypt.gensalt()).decode('utf-8'),
                    
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
    def add_user_log(user_log: UserLogEntity):
        session = SessionLocal()
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
            session.commit()  
            return user_log  
        except Exception as e:  
            session.rollback()  
            raise UserLogDatabaseError()  

    @staticmethod
    def delete_from_date_user_log(date_str):
        session = SessionLocal()
        from models.users.exceptions import UserLogDatabaseError  
        try:
            flag = int()
            date_tmp = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')  
            from_date = datetime(date_tmp.year, date_tmp.month, date_tmp.day, date_tmp.hour, date_tmp.minute, date_tmp.second)
            for user_log in UserLog.query.all():
                user_log_date = datetime.strptime(user_log.user_log_date, '%d/%m/%Y %H:%M:%S')
                if user_log_date <= from_date:  
                    session.delete(user_log)  
                    session.commit()  
                    flag += 1
            return flag  
        except Exception as e:  
            session.rollback()  
            raise UserLogDatabaseError()

    @staticmethod
    def delete_all_user_log():
        session = SessionLocal()
        from models.users.exceptions import UserLogDatabaseError  
        try:
            UserLog.query.delete()  
            session.commit()  
        except Exception as e:  
            session.rollback()  
            raise UserLogDatabaseError()  

    @staticmethod
    def get_user_logs():
        from models.users.exceptions import UserLogError  
        try:
            r_list = []  
            user_logs = UserLog.query.order_by(UserLog.user_log_date.desc()).all()  
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
