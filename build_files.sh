#!/bin/bash
echo "BUILD START"
# Upgrade pip
python3.9 -m pip install --upgrade pip

# Install dependencies
python3.9 -m pip install -r requirements.txt

# Collect static files
python3.9 manage.py collectstatic --noinput

# Make migrations
python3.9 manage.py makemigrations

# Apply migrations
python3.9 manage.py migrate

echo "BUILD END"
