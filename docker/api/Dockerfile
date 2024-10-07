# 1. Use the official Ubuntu image
FROM ubuntu:latest

# 2. Set the working directory
WORKDIR /app

# 3. Update the package list and install the necessary packages like Python 3, Python 3 pip, Python 3 venv, ping, MariaDB client, and MariaDB development libraries
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv iputils-ping mariadb-client libmariadb-dev && \
    apt-get clean

# 4. Create a virtual environment
RUN python3 -m venv venv

# 5. Upgrade pip
RUN . venv/bin/activate && pip install --upgrade pip

# 6. Copy the requirements file
COPY requirements-api.txt .

# 7. Install the dependencies
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements-api.txt

# 8. Create the directories for the API, utilities, models, and entities
RUN mkdir -p ./api ./utils ./models ./entities

# 9. Copy the API, utilities, models, and entities
COPY api ./api
COPY utils ./utils
COPY models ./models
COPY entities ./entities

# 10. Establish the connection to the database
COPY ./api/connection.py ./api/connection.py
RUN . venv/bin/activate && python ./api/connection.py

# 11. Install Alembic
RUN . venv/bin/activate && pip install alembic
COPY alembic ./alembic
COPY alembic.ini .

# 12. Update the env.py and alembic.ini files and create the migration script
COPY ./api/setup.py ./api/setup.py
RUN . venv/bin/activate && python ./api/setup.py && pip install mariadb && pip install --upgrade sqlalchemy

# 13. Run the migration script
RUN . venv/bin/activate && alembic revision --autogenerate -m "Migration to MariaDB"

# 14. Upgrade the database migration
RUN . venv/bin/activate && alembic upgrade head

# 15. Expose the port 8080
EXPOSE 8080

# 16. Run the FastAPI application
CMD ["/bin/bash", "-c", ". venv/bin/activate && uvicorn api:fastapi_app --host 0.0.0.0 --port 8080 --workers 6 --reload"]
