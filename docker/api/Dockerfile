FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev gcc mariadb-client && \
    rm -rf /var/lib/apt/lists/*

COPY api/ api/
COPY alembic.ini .
COPY utils/ utils/
COPY start_api.py .
COPY models/ models/
COPY alembic/ alembic/
COPY entities/ entities/
COPY requirements-api.txt .

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r requirements-api.txt

CMD ["alembic", "revision", "--autogenerate", "-m", "init"]

CMD ["alembic", "upgrade", "head"]

EXPOSE 8080

CMD ["python3", "start_api.py"]
