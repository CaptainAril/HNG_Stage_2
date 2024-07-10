#!/usr/bin/bash

python3 -m venv venv
source venv/bin/activate
python3.12 -m pip install --upgrade pip
pip3 install -r requirements.txt
cd hngUser
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
# end of file

