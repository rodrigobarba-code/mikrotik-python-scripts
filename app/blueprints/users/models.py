# Description: Users Model for the Users Blueprint

# Importing Required Libraries
import bcrypt
from app.extensions import db
from datetime import datetime
# Importing Required Libraries

# Importing Required Entities
from app.blueprints.users.entities import UserEntity
from app.blueprints.users.entities import UserLogEntity
# Importing Required Entities

# Importing Required Functions
from app.blueprints.users.functions import UsersFunctions
# Importing Required Functions

# Users Model
class User(db.Model):
    __tablename__ = 'users'  # Table Name

    # Columns
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # User ID
    user_username = db.Column(db.String(128), nullable=False)  # User Username
    user_password = db.Column(db.String(128), nullable=False)  # User Password
    user_name = db.Column(db.String(128), nullable=False)  # User Name
    user_lastname = db.Column(db.String(128), nullable=False)  # User Lastname
    user_privileges = db.Column(db.String(128), nullable=False)  # User Privileges
    user_state = db.Column(db.Integer, default=1, nullable=False)  # User State
    # Columns

    # Object Representation
    def __repr__(self):
        return f'<User {self.user_id}>'  # Object Representation
    # Object Representation

    # Dictionary Representation
    def to_dict(self):
        return {
            'user_id': self.user_id,  # User ID
            'user_username': self.user_username,  # User Username
            'user_password': self.user_password,  # User Password
            'user_name': self.user_name,  # User Name
            'user_lastname': self.user_lastname,  # User Lastname
            'user_privileges': self.user_privileges,  # User Privileges
            'user_state': self.user_state  # User State
        }
    # Dictionary Representation

    # Static Methods
    # User - Add User
    @staticmethod
    def add_user(user: UserEntity):
        model_u = User  # Model User
        v_user = UsersFunctions()  # Users Functions
        try:
            # Check if the user information is valid
            if v_user.validate_user(user, "insert", model_u):
                # If everything is valid, add the user to the database
                # Encrypt the password
                hashed_password = bcrypt.hashpw(user.user_password.encode('utf-8'), bcrypt.gensalt())
                new_user = User(  # Create a new user
                    user_id=None,  # User ID
                    user_username=str(user.user_username),  # User Username
                    user_password=hashed_password,  # User Password
                    user_name=str(user.user_name),  # User Name
                    user_lastname=str(user.user_lastname),  # User Lastname
                    user_privileges=str(user.user_privileges),  # User Privileges
                    user_state=str(user.user_state)  # User State
                )
                db.session.add(new_user)  # Add the new user to the session
                db.session.commit()  # Commit the session
                # If everything is valid, add the user to the database
            else:  # If the router information is not valid
                raise Exception()  # Raise an exception
        except Exception as e:  # If any other exception occurs
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
    # User - Add User

    # User - Update User
    @staticmethod
    def update_user(new_user: UserEntity):
        try:
            model_u = User  # Model User
            v_user = UsersFunctions()  # Users Functions
            # Check if the user information is valid
            if v_user.validate_user(new_user, "update", model_u):
                # If everything is valid, update the user in the database
                # Encrypt the password
                hashed_password = bcrypt.hashpw(new_user.user_password.encode('utf-8'), bcrypt.gensalt())  # Encrypt the password
                old_user = User.query.get(new_user.user_id)  # Get the old user
                old_user.user_username = new_user.user_username  # Update the user username
                if new_user.user_password != old_user.user_password and new_user.user_password != '':  # Check if the password is different
                    old_user.user_password = hashed_password  # Update the user password
                old_user.user_name = new_user.user_name  # Update the username
                old_user.user_lastname = new_user.user_lastname  # Update the user lastname
                old_user.user_privileges = new_user.user_privileges  # Update the user privileges
                old_user.user_state = new_user.user_state  # Update the user state
                db.session.commit()  # Commit the session
            else:  # If the user information is not valid
                raise Exception()  # Raise an exception
        except Exception as e:  # If any other exception occurs
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
    # User - Update User

    # User - Delete User
    @staticmethod
    def delete_user(user_id: int):
        model_u = User  # Model User
        v_user = UsersFunctions()  # Users Functions
        try:
            # Check if the user information is valid
            if v_user.validate_user(
                    UserEntity(
                        user_id=user_id,  # User ID
                        user_username=str(),  # User Username
                        user_password=str(),  # User Password
                        user_name=str(),  # User Name
                        user_lastname=str(),  # User Lastname
                        user_privileges=str(),  # User Privileges
                        user_state=int()  # User State
                    ),
                    "delete",  # Operation
                    model_u  # Model
            ):
                # If everything is valid, delete the user from the database
                # Get the user that will be deleted
                user = User.query.get(user_id)
                db.session.delete(user)  # Delete the user
                db.session.commit()  # Commit the session
            else:  # If the user information is not valid
                raise Exception()  # Raise an exception
        except Exception as e:  # If any other exception occurs
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
    # User - Delete User

    # User - Delete All Users
    @staticmethod
    def delete_all_users():
        try:
            User.query.delete()  # Delete all users
            db.session.commit()  # Commit the session
        except Exception as e:  # If any exception occurs
            db.session.rollback()  # Rollback the session
            raise e  # Raise the exception
    # User - Delete All Users

    # User - Get User
    @staticmethod
    def get_user(user_id: int):
        model_u = User  # Model User
        v_user = UsersFunctions()  # Users Functions
        try:
            # Check if the user information is valid
            if v_user.validate_user(
                    UserEntity(
                        user_id=user_id,  # User ID
                        user_username=str(),  # User Username
                        user_password=str(),  # User Password
                        user_name=str(),  # User Name
                        user_lastname=str(),  # User Lastname
                        user_privileges=str(),  # User Privileges
                        user_state=int()  # User State
                    ),
                    "get",  # Operation
                    model_u  # Model
            ):
                # If everything is valid, get the user from the database
                # Get the user
                user = User.query.get(user_id)
                obj = UserEntity(  # Create a UserEntity object
                    user_id=user.user_id,  # User ID
                    user_username=user.user_username,  # User Username
                    user_password=bcrypt.hashpw(user.user_password, bcrypt.gensalt()).decode('utf-8'),  # Decrypt Password
                    user_name=user.user_name,  # User Name
                    user_lastname=user.user_lastname,  # User Lastname
                    user_privileges=user.user_privileges,  # User Privileges
                    user_state=user.user_state  # User State
                )
                obj.validate()  # Validate the UserEntity object
                return obj  # Return the UserEntity object
            else:  # If the user information is not valid
                raise Exception()  # Raise an exception
        except Exception as e:  # If any other exception occurs
            raise e  # Raise the exception
    # User - Get User

    # User - Get All Users
    @staticmethod
    def get_users():
        try:
            r_list = []  # User List
            users = User.query.all()  # Get all users
            for user in users:  # Loop through all users
                obj = UserEntity(  # Create a UserEntity object
                    user_id=user.user_id,  # User ID
                    user_username=user.user_username,  # User Username
                    user_password=bcrypt.hashpw(user.user_password, bcrypt.gensalt()).decode('utf-8'),
                    # Decrypt Password
                    user_name=user.user_name,  # User Name
                    user_lastname=user.user_lastname,  # User Lastname
                    user_privileges=user.user_privileges,  # User Privileges
                    user_state=user.user_state  # User State
                )
                obj.validate()  # Validate the UserEntity object
                r_list.append(obj)  # Append the UserEntity object to the User List
            return r_list  # Return the User List
        except Exception as e:  # If any exception occurs
            raise e  # Raise the exception
    # User - Get All Users
    # Static Methods
# Users Model

# User Log Model
class UserLog(db.Model):
    __tablename__ = 'users_log'  # Table Name

    # Columns
    user_log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # User Log ID
    rk_user_id = db.Column(db.Integer, nullable=False)  # Reference Key User ID
    rk_user_username = db.Column(db.String(128), nullable=False)  # Reference Key User Username
    rk_user_name = db.Column(db.String(128), nullable=False)  # Reference Key Name
    rk_user_lastname = db.Column(db.String(128), nullable=False)  # Reference Key User Lastname
    user_log_description = db.Column(db.String(256), nullable=True)  # User Log Description
    user_log_action = db.Column(db.String(128), nullable=False)  # User Log Action
    user_log_table = db.Column(db.String(128), nullable=True)  # User Log Table
    user_log_date = db.Column(db.String(128), nullable=False)  # User Log Date
    user_log_public_ip = db.Column(db.String(32), nullable=False)  # User Log Public IP
    user_log_local_ip = db.Column(db.String(32), nullable=False)  # User Log Local IP
    # Columns

    # Object Representation
    def __repr__(self):
        return f'<UserLog {self.user_log_id}>'  # Object Representation
    # Object Representation

    # Dictionary Representation
    def to_dict(self):
        return {
            'user_log_id': self.user_log_id,  # User Log ID
            'rk_user_id': self.rk_user_id,  # Reference Key User ID
            'rk_user_username': self.rk_user_username,  # Reference Key User Username
            'rk_user_name': self.rk_user_name,  # Reference Key Name
            'rk_user_lastname': self.rk_user_lastname,  # Reference Key User Lastname
            'user_log_description': self.user_log_description,  # User Log Description
            'user_log_action': self.user_log_action,  # User Log Action
            'user_log_table': self.user_log_table,  # User Log Table
            'user_log_date': self.user_log_date,  # User Log Date
            'user_log_public_ip': self.user_log_public_ip,  # User Log Public IP
            'user_log_local_ip': self.user_log_local_ip  # User Log Local IP
        }
    # Dictionary Representation

    # Static Methods
    # User Log - Add User Log
    @staticmethod
    def add_user_log(user_log: UserLogEntity):
        from app.blueprints.users.exceptions import UserLogDatabaseError  # Import UserLogDatabaseError
        try:
            new_user_log = UserLog(  # Create a new user log
                user_log_id=None,  # User Log ID
                rk_user_id=user_log.rk_user_id,  # Reference Key User ID
                rk_user_username=user_log.rk_user_username,  # Reference Key User Username
                rk_user_name=user_log.rk_user_name,  # Reference Key Name
                rk_user_lastname=user_log.rk_user_lastname,  # Reference Key User Lastname
                user_log_description=user_log.user_log_description,  # User Log Description
                user_log_action=user_log.user_log_action,  # User Log Action
                user_log_table=user_log.user_log_table,  # User Log Table
                user_log_date=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),  # User Log Date
                user_log_public_ip=user_log.user_log_public_ip,  # User Log Public IP
                user_log_local_ip=user_log.user_log_local_ip  # User Log Local IP
            )
            db.session.add(new_user_log)  # Add the new user log to the session
            db.session.commit()  # Commit the session
            return user_log  # Return the UserLogEntity object
        except Exception as e:  # If any exception occurs
            db.session.rollback()  # Rollback the session
            raise UserLogDatabaseError()  # Raise UserLogDatabaseError
    # User Log - Add User Log

    # User Log - Delete From Date User Log
    @staticmethod
    def delete_from_date_user_log(date_str):
        from app.blueprints.users.exceptions import UserLogDatabaseError  # Import UserLogDatabaseError
        try:
            flag = int()
            date_tmp = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')  # Convert date_str to a date object
            from_date = datetime(date_tmp.year, date_tmp.month, date_tmp.day, date_tmp.hour, date_tmp.minute, date_tmp.second)  # Create a datetime object
            # Loop through all user logs and delete those older than from_date
            for user_log in UserLog.query.all():  # Loop through all user logs
                # Convert user_log.user_log_date from string to datetime
                user_log_date = datetime.strptime(user_log.user_log_date, '%d/%m/%Y %H:%M:%S')
                if user_log_date <= from_date:  # Check if the user log date is older than from_date
                    db.session.delete(user_log)  # Delete the user log
                    db.session.commit()  # Commit after deleting all the necessary logs
                    flag += 1  # Set the flag to 1
            # Loop through all user logs and delete those older than from_date
            return flag  # Return the flag
        except Exception as e:  # If any exception occurs
            db.session.rollback()  # Rollback the session
            raise UserLogDatabaseError()  # Raise UserLogDatabaseError
    # User Log - Delete From Date User Log

    # User Log - Delete All User Log
    @staticmethod
    def delete_all_user_log():
        from app.blueprints.users.exceptions import UserLogDatabaseError  # Import UserLogDatabaseError
        try:
            UserLog.query.delete()  # Delete all user logs
            db.session.commit()  # Commit the session
        except Exception as e:  # If any exception occurs
            db.session.rollback()  # Rollback the session
            raise UserLogDatabaseError()  # Raise UserLogDatabaseError
    # User Log - Delete All User Log

    # User Log - Get User Logs
    @staticmethod
    def get_user_logs():
        from app.blueprints.users.exceptions import UserLogError  # Import UserLogDatabaseError
        try:
            r_list = []  # User Log List
            user_logs = UserLog.query.order_by(UserLog.user_log_date.desc()).all()  # Get all user logs
            for user_log in user_logs:  # Loop through all user logs
                obj = UserLogEntity(  # Create a UserLogEntity object
                    user_log_id=user_log.user_log_id,  # User Log
                    rk_user_id=user_log.rk_user_id,  # Reference Key User ID
                    rk_user_username=user_log.rk_user_username,  # Reference Key User Username
                    rk_user_name=user_log.rk_user_name,  # Reference Key Name
                    rk_user_lastname=user_log.rk_user_lastname,  # Reference Key User Lastname
                    user_log_description=user_log.user_log_description,  # User Log Description
                    user_log_action=user_log.user_log_action,  # User Log Action
                    user_log_table=user_log.user_log_table,  # User Log Table
                    user_log_date=user_log.user_log_date,  # User Log Date
                    user_log_public_ip=user_log.user_log_public_ip,  # User Log Public IP
                    user_log_local_ip=user_log.user_log_local_ip  # User Log Local IP
                )
                obj.validate()  # Validate the UserLogEntity object
                r_list.append(obj)  # Append the UserLogEntity object to the User Log List
            return r_list  # Return the User Log List
        except Exception as e:
            raise UserLogError()  # Raise UserLogError
    # User Log - Get User Logs
    # Static Methods
# User Log Model
