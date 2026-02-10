#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Seed currencies (critical for app to work)
python manage.py seed_currencies

python manage.py collectstatic --no-input
python manage.py migrate

# Configure Site domain for Google OAuth
python manage.py configure_site
