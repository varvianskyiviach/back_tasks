#!/bin/sh
ls /app
alembic upgrade head
python app/src/initial_data.py

echo "Starting the app..."

exec "$@"