#!/bin/bash
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:3000 app:app
