#instance config.py

SECRET_KEY                      = 'MZvKzJmUl8gN6z5jptAO'
SQLALCHEMY_DATABASE_URI         = 'sqlite:///db.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS  = True
MAX_CONTENT_LENGTH              = 10 * 1024 * 1024 * 1024 # 10 gb max

MEDIA_FOLDER                    = '/media'
TACTOCNET_FOLDER                = '/media/tactoc-net'
UPLOADS_FOLDER                   = '/media/tactoc-net/uploads'
CLOUD_FOLDER                    = '/media/tactoc-net/cloud'


#Debugging
DEBUG = True