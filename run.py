from tactocnet import app
from sys import argv


if __name__ == "__main__":
    args = {}
    args["debug"]           = False
    args["host"]            = "192.168.10.180"
    args["port"]            = 80
    args["threaded"]        = True

    if  "-ssl" in argv:
        args["port"]       = 443

    if  "-l" in argv:
        if not "-ip" in argv:
            args["host"]        = "localhost"
    if "-d" in argv:
        args["debug"]       = True

    if "-ip" in argv:
        if not "-l" in argv:
            args["host"] = "0.0.0.0"


    app.run(**args)
