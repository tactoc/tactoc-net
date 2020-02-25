from flask import Blueprint, render_template, session, current_app, send_from_directory, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from colorama import init, Fore, Back, Style
import os
import shutil
from . import app, db
from .models import Mails
main = Blueprint("main", __name__)


@main.route("/test")
def test():
    return render_template("test.html")

@main.route("/")
def index():
    return redirect(url_for("main.cloud"))

@main.route("/projects")
def projects():
    return render_template("projects.html")

@main.route("/profile")
@login_required
def profile():
    username            = current_user.username
    email               = current_user.email
    storageused         = Cloud().get_storage()
    storagelimit        = Cloud().parse_bytes(current_user.storagelimit)
    return render_template("profile.html", name=username, email=email, storagelimit=storagelimit, storageused=storageused)

@main.route("/uploads")
@login_required
def uploads():
    return render_template("uploads.html")

@main.route("/uploads/<path:filename>", methods=["GET", "POST"])
@login_required
def download_upload(filename):
    uploads = os.path.join(current_app.root_path, app.config["UPLOAD_FOLDER"])
    return send_from_directory(directory=uploads, filename=filename)

@main.route("/contact", methods=["GET", "POST"])
def contact():
    user = current_user
    
    if request.method == "POST":
        data = request.form
        usernameInput   = data["usernameInput"]
        emailInput      = data["emailInput"]
        titleInput      = data["titleInput"]
        subjectInput    = data["subjectInput"]
        print(usernameInput)
        print(emailInput)
        print(titleInput)
        print(subjectInput)
        if "" in [usernameInput,emailInput,titleInput,subjectInput]:
            flash("Please fill out all of the fields")
            return render_template("contact.html", user=user)
        
        new_mail = Mails(email=emailInput, username=usernameInput, title=titleInput, subject=subjectInput)
        
        db.session.add(new_mail)
        db.session.commit()
        flash("Your message has been sent!")


    return render_template("contact.html", user=user)



SELECTED_FOLDER = [""]

class Cloud(object):
    global SELECTED_FOLDER
    def __init__(self):
        self.username           = current_user.username
        self.storagelimit       = current_user.storagelimit
        self.cloud_path         = os.path.join(current_app.root_path, app.config["CLOUD_FOLDER"])
        ##check if folder exists
        if not os.path.exists(os.path.join(self.cloud_path, *SELECTED_FOLDER)):
            os.mkdir(os.path.join(self.cloud_path, *SELECTED_FOLDER))
        self.files              = self.get_files()

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
        if len(i) > 12:
            if typ == 0:
                return i[:12]
            elif typ == 1:
                root_ext = os.path.splitext(os.path.join(self.cloud_path, *SELECTED_FOLDER, i))
                ext = root_ext[1]
                return i[:12] + ext
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
        if not value == SELECTED_FOLDER[-1]:
            SELECTED_FOLDER.append(value)
        print(SELECTED_FOLDER)
    
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

@main.route("/cloud", methods=["GET", "POST"])
@login_required
def cloud():
    global SELECTED_FOLDER
    SELECTED_FOLDER[0] = current_user.username
    user_cloud = Cloud()
    print(SELECTED_FOLDER)

    if request.method == "POST":
        print("FORMS: ",request.form)
        if "change_root" in request.form:
            SELECTED_FOLDER = [""]
            SELECTED_FOLDER[0] = current_user.username
            user_cloud.files = user_cloud.get_files()

        if "change_folder" in request.form:
            value = request.form["change_folder"]
            user_cloud.change_folder(value)
            print(SELECTED_FOLDER)
            user_cloud.files = user_cloud.get_files()
        if "back.x" in request.form or "back.y" in request.form:
            user_cloud.go_back()
            print(SELECTED_FOLDER)
            user_cloud.files = user_cloud.get_files()


        ##files and stuff
        if "newfoldername" in request.form:
            value = request.form["newfoldername"]
            path = os.path.join(user_cloud.cloud_path, *SELECTED_FOLDER, value)
            if not os.path.exists(path):
                os.mkdir(path)
                flash("Created ", value)
                user_cloud.files = user_cloud.get_files()

        if "file_upload" in request.files:
            f = request.files["file_upload"]
            print(f)
            if f.filename == "":
                flash("No selected file")
                return redirect(url_for("main.cloud"))
            #save file
            path = os.path.join(user_cloud.cloud_path, *SELECTED_FOLDER, f.filename)
            if not os.path.exists(path):
                f.save(path)
                #Check if size is appropitate
                f_size = os.stat(path).st_size
                storage_max         = current_user.storagelimit
                storage_used        = user_cloud.get_storage_bytes()
                storage_available   = storage_max - storage_used
                if not f_size >= storage_available:
                    flash("Saved ",{f.filename})
                else:
                    os.remove(path)
                    flash("You can not exceed your ",user_cloud.parse_bytes(storage_max))

                user_cloud.files = user_cloud.get_files()
        
        if "delete" in request.form:
            value = request.form["delete"]
            path_to_file = os.path.join(user_cloud.cloud_path, *SELECTED_FOLDER, value)
            #Check if folder or file
            if os.path.splitext(path_to_file)[1] == "":
                if os.path.isdir(path_to_file):
                    shutil.rmtree(path_to_file)
                    
                if os.path.isfile(path_to_file):
                    os.remove(path_to_file)
            else:
                os.remove(path_to_file)
            user_cloud.files = user_cloud.get_files()
            flash("Removed ",{value})

        if "edit" in request.form:
            target, value = request.form["edit"].split(",")
            value = value[:12]
            print(target + value)
            #Check if folder or file
            checker = os.path.splitext(os.path.join(user_cloud.cloud_path, *SELECTED_FOLDER, target))
            try:
                if checker[1] == "":
                    os.rename(os.path.join(user_cloud.cloud_path, *SELECTED_FOLDER, target), os.path.join(user_cloud.cloud_path, *SELECTED_FOLDER, value))
                else:
                    value = value + checker[1]
                    os.rename(os.path.join(user_cloud.cloud_path, *SELECTED_FOLDER, target), os.path.join(user_cloud.cloud_path, *SELECTED_FOLDER, value))
            except:
                flash(value + " is not a valid name!")
            user_cloud.files = user_cloud.get_files()
    return render_template("cloud.html", SELECTED_FOLDER=SELECTED_FOLDER, user_cloud=user_cloud)


@main.route("/cloud/<user>/<path:filename>", methods=["GET", "POST"])
@login_required
def download_cloud(user,filename):
    user = current_user.username
    cloud = os.path.join(current_app.root_path, app.config["CLOUD_FOLDER"], user)
    return send_from_directory(directory=cloud, filename=filename)



