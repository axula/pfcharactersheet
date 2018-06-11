from flask import g
from flask_wtf import FlaskForm
from app import images, files
from user.forms import LoginForm, UserForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, \
                    PasswordField, SubmitField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import Character
import os

'''images = UploadSet('images', IMAGES)
xml = UploadSet('files', 'xml')'''

class LoginForm(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default = False)

class CharacterForm(FlaskForm):
    xml_file = FileField('XML File', validators=[DataRequired(), FileAllowed(files, 'XML files only!')])
    image_file = FileField('Portrait', validators=[FileAllowed(images, 'Images only!')])
    save = SubmitField('Save')

class EditCharacterForm(FlaskForm):
    xml_file = FileField('XML File', validators=[FileAllowed(files, 'XML files only!')])
    image_file = FileField('Portrait', validators=[FileAllowed(images, 'Images only!')])
    save = SubmitField('Update')

class AdjustmentForm(FlaskForm):
    save = SubmitField('Save')
    name = StringField('Name')
    category = StringField('Category')
    description = TextAreaField('Description')
    adjStrength = IntegerField('Str', validators=[ Optional() ])
    adjDexterity = IntegerField('Dex', validators=[ Optional() ])
    adjConstitution = IntegerField('Con', validators=[ Optional() ])
    adjIntelligence = IntegerField('Int', validators=[ Optional() ])
    adjWisdom = IntegerField('Wis', validators=[ Optional() ])
    adjCharisma = IntegerField('Cha', validators=[ Optional() ])
    # Ability Checks
    adjAbiCheck = IntegerField('Ability Checks', validators=[ Optional() ])
    adjStrCheck = IntegerField('Str Checks', validators=[ Optional() ])
    adjDexCheck = IntegerField('Dex Checks', validators=[ Optional() ])
    adjConCheck = IntegerField('Con Checks', validators=[ Optional() ])
    adjIntCheck = IntegerField('Int Checks', validators=[ Optional() ])
    adjWisCheck = IntegerField('Wis Checks', validators=[ Optional() ])
    adjChaCheck = IntegerField('Cha Checks', validators=[ Optional() ])
    # Attacks
    adjAttack = IntegerField('Attack', validators=[ Optional() ])
    adjMelee = IntegerField('Melee', validators=[ Optional() ])
    adjRanged = IntegerField('Range', validators=[ Optional() ])
    adjCMB = IntegerField('CMB', validators=[ Optional() ])
    # Defenses
    adjDef = IntegerField('Defenses', validators=[ Optional() ])
    adjAC = IntegerField('AC', validators=[ Optional() ])
    adjCMD = IntegerField('CMD', validators=[ Optional() ])
    flatfooted = BooleanField('Flatfooted?', validators=[ Optional() ])
    # Saves
    adjSaves = IntegerField('Saves', validators=[ Optional() ])
    adjFort = IntegerField('Fort', validators=[ Optional() ])
    adjRef = IntegerField('Ref', validators=[ Optional() ])
    adjWill = IntegerField('Will', validators=[ Optional() ])
    # Skills
    adjSkills = IntegerField('Skills', validators=[ Optional() ])
    # Miscellaneous
    adjInit = IntegerField('Initiative', validators=[ Optional() ])
    adjSpeed = IntegerField('Speed', validators=[ Optional() ])
