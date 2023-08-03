# checkfolder
Python Flask App running Waitress on Windows
this is for logging and show file / folders changes from the watchfolder app
Flask Migrate not setup have to manually setup the database

make a .env file in the folder
DB_SERVER = mysql+pymysql://root:password@serverIP/fileserver
SECRET_KEY = SuperSecretPassword

install python3
setup.bat will create a virtual envroment and pip install the requirements
watchfolder.bat will run the python app at port 5050
