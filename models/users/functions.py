from sqlalchemy import func
from models.users.exceptions import *

class UsersFunctions:
    def __init__(self):  
        pass
    
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
