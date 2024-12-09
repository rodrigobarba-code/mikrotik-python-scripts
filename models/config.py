import os

user = os.environ.get('DB_USER', 'sevensuiteuser')
password = os.environ.get('DB_PASSWORD', 'development-sevensuiteapp')
# host = os.environ.get('DB_HOST', 'localhost:3306')  # For Development
host = os.environ.get('DB_HOST', 'mariadb-database:3306')  # For Docker
database = os.environ.get('DB_NAME', 'sevensuite')

connection_string = f'mariadb+mariadbconnector://{user}:{password}@{host}/{database}'

class DatabaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = connection_string
