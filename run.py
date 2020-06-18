#!/usr/bin/python
# -*- coding: utf-8 -*-

from pcs import app
from sys import argv

#We use this module to run the server
if __name__ == "__main__":
    args = {}
    args["debug"]           = False
    args["host"]            = "0.0.0.0"
    args["port"]            = 80
    args["threaded"]        = True

    #Run with ssl port
    if  "-ssl" in argv:
        args["port"]       = 443

    #Run in localhost
    if  "-l" in argv:
        if not "-ip" in argv:
            args["host"]        = "localhost"

    if "-d" in argv:
        args["debug"]       = True


    app.run(**args)
