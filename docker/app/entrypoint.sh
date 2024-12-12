#!/bin/bash
set -e  # If a command fails then the entrypoint stops

# Check if the database is ready
echo "Waiting for MySQL to be ready..."
until mysql -h mariadb-database -u sevensuiteuser -pdevelopment-sevensuiteapp -e "SELECT 1" &>/dev/null; do
    echo "MySQL is unavailable - sleeping"
    sleep 1
done

# Check if the database exists
echo "Checking if the database exists..."
# Verify if not give error
if mysql -h mariadb-database -u sevensuiteuser -pdevelopment-sevensuiteapp -e "USE sevensuite;" 2>/dev/null; then
    if mysql -h mariadb-database -u sevensuiteuser -pdevelopment-sevensuiteapp -e "USE sevensuite; SHOW TABLES;" | grep -q "alembic_version"; then
        echo "Database exists and is up to date."
        echo "Starting the app..."
        exec python3 run.py
    else
        echo "Database exists but is not up to date."

        echo "Creating the migration revision..."
        alembic revision --autogenerate -m "Rebase migration"

        echo "Applying the migrations..."
        alembic upgrade head

        echo "Importing the database dump..."
        mysql -h mariadb-database -u sevensuiteuser -pdevelopment-sevensuiteapp sevensuite < api/dump.sql

        echo "Starting the app..."
        exec python3 run.py
    fi
fi








