#!/usr/bin/env bash
# Render build script

set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Collect static files
python manage.py collectstatic --no-input

# 3. Run database migrations
python manage.py migrate --no-input

# 4. TEMPORARY: Load initial data into the PostgreSQL database
# The '|| echo' part ensures the build doesn't crash if the data is already loaded on a future rebuild
python manage.py loaddata fixtures/initial_data.json || echo "Data already loaded or fixture not found, continuing..."