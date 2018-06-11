import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES, configure_uploads
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Login Manager
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# Uploads
images = UploadSet('images', IMAGES)
files = UploadSet('files', 'xml')
configure_uploads(app, (images, files))

from app import views, models
