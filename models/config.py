import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or os.getenv('MARIADB_CONNECTION_STRING')
