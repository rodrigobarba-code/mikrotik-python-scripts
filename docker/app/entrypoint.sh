#!/bin/bash
set -e  # If a command fails then the entrypoint stops

echo "Waiting for MySQL to be ready..."
until mysql -h mariadb-database -u sevensuiteuser -pdevelopment-sevensuiteapp -e "SELECT 1" &>/dev/null; do
  sleep 2
done

echo "Creating the database if it does not exist..."
mysql -h mariadb-database -u sevensuiteuser -pdevelopment-sevensuiteapp -e "CREATE DATABASE IF NOT EXISTS sevensuite;"

echo "Applying the migrations..."
alembic revision --autogenerate -m "Rebase migration"
alembic upgrade head

echo "Importing the database dump..."
mysql -h mariadb-database -u sevensuiteuser -pdevelopment-sevensuiteapp sevensuite < api/dump.sql

echo "Starting the app..."
exec python3 run.py
