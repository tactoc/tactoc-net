import os
import sys
HOST        = "localhost"
PORT        = 80

if __name__ == "__main__":
    args = sys.argv[1:]
    os.environ['FLASK_APP'] = '__init__'
    if '-d' in args or 'debug' in args:
        print('DEBUG = TRUE')
        os.environ['FLASK_DEBUG'] = "1"
    os.system(f'flask run -h {HOST} -p {PORT}')