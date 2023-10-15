#!/bin/bash

#Build the project
echo "Building the project..."
python3.9 -m pip install -r requirements.txt

echo "Make Migration..."
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinout

echo "Collect Station.."
python3.9 manage.py collectstatic --noinput --clear
