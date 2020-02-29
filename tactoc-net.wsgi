import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/tactoc-net/")

from tactoc-net import app as application
application.secret_key = 'roottactocstudios21035287'
