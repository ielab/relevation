#! /bin/sh

source ~/.bashrc
gunicorn --timeout 300 -w 2 -k gevent -b 0.0.0.0:8088 relevation.wsgi
