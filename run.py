from tactocnet import app
from sys import argv


if __name__ == "__main__":
    args = {}
    args["debug"]           = False
    args["host"]            = "192.168.10.180"
    args["port"]            = 80
    args["threaded"]        = True

    if  "-l" in argv:
        args["host"]        = "localhost"
    if "-d" in argv:
        args["debug"]       = True



    
    app.run(**args)