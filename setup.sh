#!/bin/bash
echo "Setting up Django settings module..."
export DJANGO_SETTINGS_MODULE=config.settings

echo "Running makemigrations..."
python3 manage.py makemigrations

echo "Applying migrations..."
python3 manage.py migrate

echo "Migrations applied successfully."
touch common/__init__.py

