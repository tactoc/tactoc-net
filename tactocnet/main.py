#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask,Markup,Blueprint, render_template, session, current_app, send_file ,send_from_directory, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user, logout_user
import os
import shutil
import zipfile
import ntpath
from io import BytesIO
from . import app, db
from .models import Mails
from .models import Users

main = Blueprint("main", __name__)

def print_d(s):
    if app.config["DEBUG_PRINT"]:
        print(current_user.username.upper() + " | " + str(s))


@main.route("/")
def index():
    return redirect(url_for("main.cloud"))

@main.route("/projects")
def projects():
    return render_template("/main/projects.html")

@main.route("/profile")
@login_required
def profile():
    username            = current_user.username
    email               = current_user.email
    storageused         = Cloud().get_storage()
    storagelimit        = Cloud().parse_bytes(current_user.storagelimit)
    return render_template("/main/profile.html", name=username, email=email, storagelimit=storagelimit, storageused=storageused)

@main.route("/contact", methods=["GET", "POST"])
def contact():
    user = current_user
    
    if request.method == "POST":
        data = request.form
        usernameInput   = data["usernameInput"]
        emailInput      = data["emailInput"]
        titleInput      = data["titleInput"]
        subjectInput    = data["subjectInput"]
        if "" in [usernameInput,emailInput,titleInput,subjectInput]:
            flash("Please fill out all of the fields")
            return render_template("contact.html", user=user)
        
        new_mail = Mails(email=emailInput, username=usernameInput, title=titleInput, subject=subjectInput)
        
        db.session.add(new_mail)
        db.session.commit()
        flash("Your message has been sent!")
    return render_template("/main/contact.html", user=user)

class Uploads(object):
    def __init__(self):
        self.permission     = self.get_permission()
        self.uploads_path   = app.config["UPLOADS_FOLDER"]
        self.files          = self.get_files()
    
    def update_directory(self):
        self.files          = self.get_files()
    
    def get_permission(self):
        logged_user = current_user.username
        users = Users.query.all()
        for i in users:
            if i.username == logged_user:
                return i.permission_level
        return 0

    def get_files(self):
        path = self.uploads_path
        generator = os.walk(path)
        files = []
        for i in generator:
            files.append(i)
        return files

    def parse_bytes(self,B):
        B   = float(B)
        KB  = float(1024)
        MB  = float(KB ** 2)
        GB  = float(KB ** 3)
        TB  = float(KB ** 4)
        if B < KB:
            return "{0} {1}".format(int(B) if B > 0 else "Empty" ,"B" if B > 0 else "")
        elif KB <= B < MB:
            return "{0} KB".format(round(int(B)/int(KB)))
        elif MB <= B < GB:
            return "{0} MB".format(round(int(B)/int(MB)))
        elif GB <= B < TB:
            return "{0} GB".format(round(int(B)/int(GB)))
        elif TB <= B:
            return "{0} TB".format(round(int(B)/int(TB)))

    def get_size(self,i):
        path = os.path.join(self.uploads_path, i)
        fileinfo = os.stat(path)
        return self.parse_bytes(fileinfo.st_size)

    def has_files(self):
        generator = os.listdir(self.uploads_path)
        files = []
        for i in generator:
            files.append(i)
        if len(files) > 0:
            return True
        return False

    def parse_filename(self,i):
        file_path = os.path.join(self.uploads_path,i)
        cut = 14
        if len(i) > cut:
            file = os.path.splitext(file_path)
            ext = file[1]
            name = ntpath.basename(file[0])[:cut]
            return name + ext
        return i

    def count_files(self):
        count = 0
        for i in os.listdir(self.uploads_path):
            count += 1
        return count

@main.route("/uploads", methods=["GET", "POST"])
@login_required
def uploads():
    upload_obj = Uploads()


    if request.method == "POST":

        if "delete_upload" in request.form:
            value = request.form["delete_upload"]
            path_to_file = os.path.join(upload_obj.uploads_path, value)

            os.remove(path_to_file)
            upload_obj.update_directory()
            flash("Removed " + value)

        if "edit_upload" in request.form:
            target, value = request.form["edit_upload"].split(",")
            #Check if folder or file
            ext = os.path.splitext(os.path.join(upload_obj.uploads_path, target))[1]
            try:
                os.rename(os.path.join(upload_obj.uploads_path, target), os.path.join(upload_obj.uploads_path, value + ext))
            except Exception as e:
                flash(value + " is not a valid name!")
            upload_obj.update_directory()

        if "file_upload_upload" in request.files:
            files = request.files.getlist('file_upload_upload')

            if len(files) < 1:
                flash("No selected files")
                return redirect(url_for("main.uploads"))
            #save file
            for i in files:
                f = i.filename
                path = os.path.join(upload_obj.uploads_path, f)
                if not os.path.exists(path):
                    path = Markup.escape(path)
                    i.save(path)
                    flash("Saved ",f)

            upload_obj.update_directory()


    return render_template("/main/uploads.html", obj=upload_obj)

@main.route("/uploads/<path:filename>", methods=["GET", "POST"])
@login_required
def download_upload(filename):
    uploads = os.path.join(current_app.root_path, app.config["UPLOADS_FOLDER"])
    return send_from_directory(directory=uploads, filename=filename)


SELECTED_FOLDER = [""]

class Cloud(object):
    global SELECTED_FOLDER
    def __init__(self):
        self.username           = current_user.username
        self.storagelimit       = current_user.storagelimit
        self.cloud_path         = app.config["CLOUD_FOLDER"]
        ##check if folder exists
        if not os.path.exists(os.path.join(self.cloud_path, *SELECTED_FOLDER)):
            os.mkdir(os.path.join(self.cloud_path, *SELECTED_FOLDER))
        self.files              = self.get_files()

        

    def update_directory(self):
        self.files = self.get_files()


    def download_file(self,i):
        return os.path.join("cloud",*SELECTED_FOLDER, i)

    def parse_bytes(self,B):
        B   = float(B)
        KB  = float(1024)
        MB  = float(KB ** 2)
        GB  = float(KB ** 3)
        TB  = float(KB ** 4)
        if B < KB:
            return "{0} {1}".format(int(B) if B > 0 else "Empty" ,"B" if B > 0 else "")
        elif KB <= B < MB:
            return "{0} KB".format(round(int(B)/int(KB)))
        elif MB <= B < GB:
            return "{0} MB".format(round(int(B)/int(MB)))
        elif GB <= B < TB:
            return "{0} GB".format(round(int(B)/int(GB)))
        elif TB <= B:
            return "{0} TB".format(round(int(B)/int(TB)))


    def parse_filename(self,i, typ):
        file_path = os.path.join(self.cloud_path, *SELECTED_FOLDER, i)
        cut = 14
        if len(i) > cut:
            if typ == 0:
                return i[:cut]
            elif typ == 1:
                file = os.path.splitext(file_path)
                ext = file[1]
                name = ntpath.basename(file[0])[:cut]
                return name + ext
        return i


    def get_storage(self):
        total_size = 0
        path = os.path.join(self.cloud_path, self.username)
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)

                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        return self.parse_bytes(total_size)
    
    def get_storage_bytes(self):
        total_size = 0
        path = os.path.join(self.cloud_path, self.username)
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)

                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        return total_size

    def get_storage_limit(self):
        return self.parse_bytes(self.storagelimit)

    def get_size(self,i):
        path = os.path.join(self.cloud_path, *SELECTED_FOLDER, i)
        fileinfo = os.stat(path)
        if os.path.isdir(path):
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
            return self.parse_bytes(total_size)
        return self.parse_bytes(fileinfo.st_size)



    def change_folder(self, value):
        #If value is valid change folder
        if SELECTED_FOLDER[0] == current_user.username:
            if value in self.get_files()[0][1]:
                SELECTED_FOLDER.append(value)


    
    def get_folder(self):
        return SELECTED_FOLDER[-1]
    
    def show_selected_folder(self):
        if not len(SELECTED_FOLDER) >= 3:
            return "/".join(SELECTED_FOLDER)
        dots = "../"
        return dots + "/".join(SELECTED_FOLDER[-2:])
    
    def get_files(self):
        path = os.path.join(self.cloud_path, *SELECTED_FOLDER)
        generator = os.walk(path)
        files = []
        for i in generator:
            files.append(i)
        return files



    def has_files(self):
        generator = os.listdir(os.path.join(self.cloud_path, *SELECTED_FOLDER))
        files = []
        for i in generator:
            files.append(i)
        if len(files) > 0:
            return True
        return False

    def not_files(self):
        generator = os.listdir(os.path.join(self.cloud_path, *SELECTED_FOLDER))
        files = []
        for i in generator:
            files.append(i)
        if len(files) > 0:
            return False
        return True

    def go_back(self):
        if not len(SELECTED_FOLDER) == 1:
            del SELECTED_FOLDER[-1]
    
    def zip_folder(self, i):
        path = os.path.join(self.cloud_path,*SELECTED_FOLDER, i)
        memory_zip = BytesIO()

        with zipfile.ZipFile(memory_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(path):

                for f in files:
                    dir_path = os.path.dirname(root)
                    zipf.write(os.path.join(root,f), os.path.join(dir_path, f))
        memory_zip.seek(0)
        return memory_zip


@main.route("/cloud", methods=["GET", "POST"])
@login_required
def cloud():
    global SELECTED_FOLDER
    SELECTED_FOLDER[0] = current_user.username
    print_d(SELECTED_FOLDER)
    user_cloud = Cloud()
    if request.method == "POST":
        print_d(request.form)
        if "change_root" in request.form:
            SELECTED_FOLDER = [""]
            SELECTED_FOLDER[0] = current_user.username
            user_cloud.update_directory()

        if "change_folder" in request.form:
            value = request.form["change_folder"]
            user_cloud.change_folder(value)
            user_cloud.update_directory()
            print_d("CHANGE FOLDER" + value)

        if "back.x" in request.form or "back.y" in request.form:
            user_cloud.go_back()
            user_cloud.update_directory()

        if "newfoldername" in request.form:
            value = request.form["newfoldername"]
            path = os.path.join(user_cloud.cloud_path, *SELECTED_FOLDER, value)
            print_d("NEW FOLDER PATH " + path)
            try:
                if not os.path.exists(path):
                    print_d("NEW FOLDER " + value + " PATH " + path)
                    os.mkdir(path)
                    flash("Created ", value)
                    user_cloud.update_directory()
            except Exception as e:
                print_d(e)
                flash(value + " is not a valid folder name!")

        if "file_upload" in request.files:
            files = request.files.getlist('file_upload')
            print_d("FILES" + str(files))

            if len(files) < 1:
                flash("No selected files")
                return redirect(url_for("main.cloud"))
            #save file
            for i in files:
                f = i.filename
                path = os.path.join(user_cloud.cloud_path, *SELECTED_FOLDER, f)
                print_d("FILE PATH " + path)
                if not os.path.exists(path):
                    i.save(path)
                    print_d("SAVE FILE " + f + " PATH " + path)
                    #Check if size is appropitate
                    f_size = os.stat(path).st_size
                    storage_max         = current_user.storagelimit
                    storage_used        = user_cloud.get_storage_bytes()
                    storage_available   = storage_max - storage_used
                    if not f_size >= storage_available:
                        flash("Saved ",f)
                    else:
                        
                        os.remove(path)
                        flash("You can not exceed your ",user_cloud.parse_bytes(storage_max))


            user_cloud.update_directory()
        
        if "folders_upload" in request.files:
            folder_upload = request.files.getlist('folders_upload')
            print_d("FOLDERS UPLOAD " + str(folder_upload))
            
            if folder_upload == "":
                return redirect(url_for("main.cloud"))

            path = os.path.join(user_cloud.cloud_path, *SELECTED_FOLDER)
            print_d("FOLDER PATH " + path)
            #main folder
            for f in folder_upload:
                s_file                = f.filename
                s_directories         = os.path.dirname(s_file).split("/")
                d_file                = os.path.join(path, s_file).replace("\\","/")
                if "&#39;" in d_file:
                    flash("Folders containing ' is not allowed")
                    break
                print_d("FOLDER DIRECTORIES " + str(s_directories))
                print_d("FOLDER FILE " + d_file)
                #Create all directories
                for i in s_directories:
                    if not os.path.exists(os.path.join(path, *s_directories)):
                        os.makedirs(os.path.join(path, *s_directories))
                #Save all files
                if not os.path.exists(d_file):
                    print_d("SAVE FOLDER " + s_file + " PATH " + d_file)
                    f.save(d_file)

            user_cloud.update_directory()
        
        if "delete" in request.form:
            value = request.form["delete"]
            print_d("DELETE VALUE " + value)
            path_to_file = os.path.join(user_cloud.cloud_path, *SELECTED_FOLDER, value)
            print_d("DELETE PATH " + path_to_file)
            #Check if folder or file
            if os.path.splitext(path_to_file)[1] == "":
                if os.path.isdir(path_to_file):
                    shutil.rmtree(path_to_file)
                    
                if os.path.isfile(path_to_file):
                    os.remove(path_to_file)
            else:
                print_d("DELETE " + value + " PATH " + path_to_file)
                os.remove(path_to_file)
            user_cloud.update_directory()
            flash("Removed " + value)

        if "edit" in request.form:
            target, value = request.form["edit"].split(",")
            print("EDIT " + target + " " + value)
            #Check if folder or file
            checker = os.path.splitext(os.path.join(user_cloud.cloud_path, *SELECTED_FOLDER, target))
            try:
                if checker[1] == "":
                    print_d("EDIT: TARGET " + target + " VALUE " + value)
                    os.rename(os.path.join(user_cloud.cloud_path, *SELECTED_FOLDER, target), os.path.join(user_cloud.cloud_path, *SELECTED_FOLDER, value))
                else:
                    value = value + checker[1]
                    print_d("EDIT TARGET " + target + " VALUE " + value)
                    os.rename(os.path.join(user_cloud.cloud_path, *SELECTED_FOLDER, target), os.path.join(user_cloud.cloud_path, *SELECTED_FOLDER, value))
            except Exception as e:
                flash(value + " is not a valid name!")
            user_cloud.update_directory()
    
        if "zip_folder" in request.form:
            value = request.form["zip_folder"]
            path = os.path.join(user_cloud.cloud_path, *SELECTED_FOLDER, value)
            print_d("ZIP " + str(value) + " " + path)
            memory_file = user_cloud.zip_folder(path)
            foldername = value + ".zip"
            return send_file(memory_file, attachment_filename=foldername, as_attachment=True)
    
    return render_template("/main/cloud.html", SELECTED_FOLDER=SELECTED_FOLDER, user_cloud=user_cloud)



@main.route("/cloud/<user>/<path:filename>", methods=["GET", "POST"])
@login_required
def download_cloud(user,filename):
    user = current_user.username
    cloud = os.path.join(current_app.root_path, app.config["CLOUD_FOLDER"], user)
    return send_from_directory(directory=cloud, filename=filename)


