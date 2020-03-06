#instance config.py
SECRET_KEY                      = 'MZvKzJmUl8gN6z5jptAO'
SQLALCHEMY_DATABASE_URI         = 'sqlite:///db.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS  = True
MAX_CONTENT_LENGTH              = 100 * 1024 * 1024 * 1024 # 10 gb max

MEDIA_FOLDER                    = '/media'
TACTOCNET_FOLDER                = '/media/tactocnet'
UPLOADS_FOLDER                  = '/media/tactocnet/uploads'
CLOUD_FOLDER                    = '/media/tactocnet/cloud'

#Debugging
DEBUG_PRINT                     = False

