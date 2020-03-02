#instance config.py

SECRET_KEY                      = 'MZvKzJmUl8gN6z5jptAO'
SQLALCHEMY_DATABASE_URI         = 'sqlite:///db.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS  = True
MAX_CONTENT_LENGTH              = 10 * 1024 * 1024 * 1024 # 10 gb max

MEDIA_FOLDER                    = '/home/pi/media'
TACTOCNET_FOLDER                = '/home/pi/media/tactocnet'
UPLOADS_FOLDER                   = '/home/pi/media/tactocnet/uploads'
CLOUD_FOLDER                    = '/home/pi/media/tactocnet/cloud'

