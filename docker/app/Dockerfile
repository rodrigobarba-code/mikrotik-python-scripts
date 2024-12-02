FROM python:3.10-slim

WORKDIR /sevensuite

COPY requirements-app.txt .

RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements-app.txt --no-cache-dir

COPY app/ app/
COPY entities/ entities/
COPY websockets/ websockets/
COPY start_app.py .

EXPOSE 5000

CMD ["sh", "-c", ". venv/bin/activate && python3 start_app.py"]