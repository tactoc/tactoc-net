import os
import sys
HOST        = "192.168.10.180"
PORT        = 443

if __name__ == "__main__":
    args = sys.argv[1:]
    os.environ['FLASK_APP'] = '__init__.py'
    if '-d' in args or '--debug' in args:
        print('DEBUG = TRUE')
        os.environ['FLASK_DEBUG'] = "1"
    if '-l' in args or '--localhost' in args:
        HOST = "localhost"
    
    os.system(f"flask run -h {HOST} -p {PORT} --cert=cert.pem --key=key.pem  --with-threads")
