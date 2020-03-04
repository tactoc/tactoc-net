#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask,Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Users, Codes
from . import db
import re
import datetime
auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    if not current_user.is_authenticated:
        return render_template("/auth/login.html")
    return redirect(url_for('main.cloud'))

@auth.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username").lower()
    password = request.form.get("password")

    user = Users.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash("Invalid Credentials")
        return redirect(url_for("auth.login"))

    login_user(user)
    
    return redirect(url_for("main.cloud"))
    


@auth.route("/signup")
def signup():
    return render_template("/auth/signup.html")

@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email").lower()
    username = request.form.get("username").lower()
    password = request.form.get("password")
    uniquecode = request.form.get("uniquecode")


    user_email      = Users.query.filter_by(email=email).first()
    user_username   = Users.query.filter_by(username=username).first()
    code = Codes.query.filter_by(code=uniquecode).first()

    #check email
    regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if not re.search(regex, email):
        flash("Please enter a valid email address")
        return redirect(url_for("auth.signup"))

    if not len(username) > 4:
        flash("Your username must be at least 4 characters long.")
        return redirect(url_for("auth.signup"))
    if not len(password) > 4:
        flash("Your password must be at least 4 characters long.")
        return redirect(url_for("auth.signup"))



    if user_email:
        flash("Email already exists!")
        return redirect(url_for("auth.signup"))
    if user_username:
        flash("Username already exists!")
        return redirect(url_for("auth.signup"))
    if not code:
        flash("Wrong code")
        return redirect(url_for("auth.signup"))
    
    storagelimit = 5368709120 #5 GB in bytes
    date_of_creation = datetime.datetime.now()

    
    new_user = Users(email=email, username=username, password=generate_password_hash(password, method="sha256"),storagelimit=storagelimit, date_of_creation=date_of_creation, permission_level=0)
    

    db.session.add(new_user)
    db.session.delete(code)
    db.session.commit()
    login_user(new_user)

    return redirect(url_for("auth.login"))

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
