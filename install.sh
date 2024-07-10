#!/usr/bin/bash

python3 -m venv venv
source venv/bin/activate
python3.12 -m pip install --upgrade pip
pip3 install -r requirements.txt
python3 hngUser/manage.py runserver
