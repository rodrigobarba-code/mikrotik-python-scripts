import time
from sqlalchemy import create_engine

DATABASE_URL = "mariadb+mariadbconnector://sevensuiteuser:development-sevensuiteapp@localhost:3307/sevensuite"

while True:
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()

        print("Connection successful")

        time.sleep(5)
        break
    except Exception as e:
        print(f"Conection error: {e}")
