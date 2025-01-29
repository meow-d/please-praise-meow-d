#!/bin/bash
pip3 install -r requirements.txt
python3 app.py
# gunicorn -w 4 -b 0.0.0.0:3000 app:app
