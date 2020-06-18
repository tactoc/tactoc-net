#instance config.py
SECRET_KEY                      = 'yoursecretkey'
SQLALCHEMY_DATABASE_URI         = 'sqlite:///db.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS  = True
MAX_CONTENT_LENGTH              = 100 * 1024 * 1024 * 1024 # 10 gb max

MEDIA_FOLDER                    = '/media'
PCS_FOLDER                      = '/media/pcs'
UPLOADS_FOLDER                  = '/media/pcs/uploads'
CLOUD_FOLDER                    = '/media/pcs/cloud'

#Debugging
DEBUG_PRINT                     = False

