# Private-Cloud-Service
A project i made since i wanted my own personal cloud server. You can run it on a VPS or your own Raspberry pi.
Dependencies: `flask, flask_sqlalchemy, flask_login`<br>
the run.py module makes it easy to start the server,<br>
it accepts arguments as -d (Debug) -l (Localhost) -ssl (port 443)
Example: `python run.py -l -d`

You can register and login and see your authenticated files and folders. All of the data from the users is stored in a 
root folder at `/media/pcs/` where there is two folders. There is a cloud folder and uploads folder. 
The cloud folder is where all the files from the users is located in subfolders, 
and the uploads folder is where the administrator can upload public files that all download.

The config file in `instance/config.py` contains the folder locations and other settings.

The user has the functionality to upload, edit and download files from the cloud.

The server uses a sqlite3 database with a users table with the columns:
- id
- email
- username
- password
- storagelimit
- date_of_creation
- permission_level
<br>
All users start with 5 gb of available storage on signup (You can ofc change this)
The permission level has to be changed manually in the database to give the user permission to upload to the public folder.
you can do it with this command <br>
SQL"`UPDATE users SET permission_level=1 where id={USER ID};`" 


Be aware it lacks comments in some places, but hope it is somewhat understandable.

# Screenshots
![1](https://i.imgur.com/zHBasax.png)
![2](https://i.imgur.com/Xrl1X3k.png)
