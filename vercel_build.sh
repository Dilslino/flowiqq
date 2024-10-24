#!/bin/bash
echo "Building project packages..."
echo "Installing project requirements..."
python3 -m pip install -r requirements.txt

echo "Installing psycopg2-binary..."
python3 -m pip install psycopg2-binary==2.9.6

echo "Migrating Database..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collecting static files..."
python3 manage.py collectstatic --noinput
