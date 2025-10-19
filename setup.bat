#!/bin/bash

# Navigate to your Django project directory if not already there
# For example:
# cd /path/to/your/project

echo "Running makemigrations..."
python3 manage.py makemigrations

echo "Applying migrations..."
python3 manage.py migrate

echo "Migrations applied successfully."
