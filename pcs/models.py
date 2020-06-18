#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import db
from flask_login import UserMixin
class Users(UserMixin,db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    email               = db.Column(db.String(50), unique=True)
    username            = db.Column(db.String(50), unique=True)
    password            = db.Column(db.String(50))
    storagelimit       = db.Column(db.Integer)
    date_of_creation    = db.Column(db.String(100))
    permission_level    = db.Column(db.Integer)
