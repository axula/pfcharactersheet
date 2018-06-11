import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = "na-na-na-na-na-na-na-na-na-na-BATMAN"

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'app/uploads')
