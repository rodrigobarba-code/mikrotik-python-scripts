FROM python:3.12-slim

WORKDIR /sevensuite

RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev gcc mariadb-client libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

COPY run.py .
COPY mac.txt .
COPY api/ api/
COPY app/ app/
COPY alembic.ini .
COPY utils/ utils/
COPY start_api.py .
COPY start_app.py .
COPY api/dump.sql .
COPY models/ models/
COPY requirements.txt .
COPY entities/ entities/
COPY websockets/ websockets/
COPY alembic/env.py alembic/env.py
COPY alembic/script.py.mako alembic/script.py.mako

COPY docker/app/entrypoint.sh /entrypoint.sh

RUN mkdir -p alembic/versions

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    chmod +x /entrypoint.sh

EXPOSE 8080
EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]
