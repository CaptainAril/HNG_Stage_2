#!/usr/bin/bash

echo "Setting up Virtual env..."
python3 -m venv venv
source venv/bin/activate

echo "Building project packages...."
python3.12 -m pip install --upgrade pip
pip3 install -r requirements.txt
cd hngUser

echo "Migrating Databases...."
python3 manage.py makemigrations
python3 manage.py migrate

echo "Running server...."
python3 manage.py runserver
# end of file

