#!/usr/bin/python
import sys
import logging
import flask
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/pcs/")

from tactocnet import app as application
application.secret_key = 'yoursecretkey'
