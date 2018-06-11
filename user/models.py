from app import db, images
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash
import os, uuid

class UserBase(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(256))
    role = db.Column(db.Integer)
    avatar = db.Column(db.String(256))

    # Account Settings
    private = db.Column(db.Boolean, default=False)

    def __init__(self, name, email, password, role=3):
        self.username = name
        self.email = email
        self.role = role
        self.set_password(password)
        self.save()

    @classmethod
    def get_user(cls, name):
        return cls.query.filter(
            func.lower(cls.username) == func.lower(name)
        ).first()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_avatar(self, image):
        filename = images.save(image, name=str(uuid.uuid4().hex)+'.')
        if self.avatar:
            os.remove(images.path(self.avatar))
        self.avatar = filename
        #self.squarePortrait();
        self.save()

    def avatar_url(self):
        if self.avatar:
            return images.url(self.avatar)
        else:
            return '/static/default.png'

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id) # python 2
        except NameError:
            return str(self.id) # python 3

    def __repr__(self):
        return '<User %r>' % (self.username)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        if self.avatar:
            os.remove(images.path(self.avatar))
        db.session.delete(self)
        db.session.commit()
