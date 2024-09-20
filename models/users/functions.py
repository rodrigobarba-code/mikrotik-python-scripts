from flask import session
from sqlalchemy import func
from datetime import datetime
from models.users.exceptions import *
from entities.user_log import UserLogEntity

class UsersFunctions:
    def __init__(self):  
        pass

    @staticmethod
    def create_log(user_id, description, action, table):
        from models.users.models import UserLog
        user_log = UserLogEntity(
            user_log_id=int(),
            rk_user_id=int(user_id),
            rk_user_username=str(session['user_username']),
            rk_user_name=str(session['user_name']),
            rk_user_lastname=str(session['user_lastname']),
            user_log_description=str(description),
            user_log_action=str(action),
            user_log_table=str(table),
            user_log_date=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            user_log_public_ip=str(session['user_public_ip']),
            user_log_local_ip=str(session['user_local_ip'])
        )
        user_log.validate()  
        UserLog.add_user_log(user_log)
    
    @staticmethod
    def validate_user(session, user, operation, model) -> bool:
        try:
            if operation in ["insert", "update"]:  
                if operation == "update":  
                    existing_user = session.query(model).get(user.user_id)
                    if not existing_user:  
                        raise UserNotFound(user.user_id)
                if session.query(model).filter(func.lower(model.user_username) == func.lower(user.user_username)).first() and \
                        session.query(model).filter(func.lower(model.user_username) == func.lower(user.user_username)).first().user_id != user.user_id:
                    raise UserAlreadyExists(  
                        user_id=session.query(model).filter(
                            func.lower(model.user_username) == func.lower(user.user_username)).first().user_id,
                        user_username=user.user_username  
                    )
                return True
            elif operation in ["delete", "get"]:  
                if not session.query(model).filter_by(user_id=user.user_id).first():
                    raise UserNotFound(user.user_id)  
                return True  
            return False  
        except (UserNotFound, UserAlreadyExists) as e:  
            raise e  
        except Exception:  
            raise UserError()  

    @staticmethod
    def validate_bulk_delete(session, model, user_ids):
        try:
            if not session.query(model).filter(model.user_id.in_(user_ids)).all():
                raise UserNotFound(user_ids)
            return True
        except UserNotFound as e:
            raise e

users_functions = UsersFunctions()
