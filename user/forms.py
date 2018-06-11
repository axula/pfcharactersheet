from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Optional
from app import images
from flask_wtf.file import FileField, FileAllowed
from app.models import User
import re, struct

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    def validate(self):
        self.user = None
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        user = User.get_user(self.username.data)
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True

class NewUserForm(FlaskForm):
    username = StringField('Username', validators=[\
                        DataRequired(), \
                        Length(min=4, max=20) ])
    password = PasswordField('New Password', validators=[\
                        DataRequired(), Length(min=6, max=35), \
                        EqualTo('confirm', message="Passwords must match") ])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(min=6, max=35)])
    save = SubmitField('Save Changes')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        user = User.get_user(self.username.data)
        if user and user.username.lower() != g.user.username.lower():
            self.username.errors.append('Username already in use')
            return False

        return True

class UserForm(FlaskForm):
    username = StringField('Username', validators=[\
                        DataRequired(), \
                        Length(min=4, max=20) ])
    old_password = PasswordField('Old Password')
    password = PasswordField('New Password', validators=[\
                        Optional(), Length(min=6, max=35), \
                        EqualTo('confirm', message="Passwords must match") ])
    confirm = PasswordField('Repeat Password')
    email = StringField('Email', validators=[DataRequired(), Length(min=6, max=35)])
    avatar = FileField('Avatar', validators=[FileAllowed(images, 'Images only!')])
    save = SubmitField('Save Changes')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        user = User.get_user(self.username.data)
        if user and user.username.lower() != g.user.username.lower():
            self.username.errors.append('Username already in use')
            return False

        if self.password.data:
            if self.old_password.data == '':
                self.old_password.errors.append('Please enter your old password')
                return False
            elif not user.check_password(self.old_password.data):
                self.old_password.errors.append('Incorrect password')
                return False

        return True
