from flask import g
from flask_wtf import FlaskForm
from app import images, files
from user.forms import LoginForm, UserForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, PasswordField
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
	xml_file = FileField('XML File', validators=[ FileAllowed(files, 'XML files only!') ])
	image_file = FileField('Portrait', validators=[FileAllowed(images, 'Images only!')])

class AdjustmentForm(FlaskForm):
	name = StringField('name')
	category = StringField('category')
	description = TextAreaField('description')
	adjStrength = IntegerField('adjStr', validators=[ Optional() ])
	adjDexterity = IntegerField('adjDex', validators=[ Optional() ])
	adjConstitution = IntegerField('adjCon', validators=[ Optional() ])
	adjIntelligence = IntegerField('adjInt', validators=[ Optional() ])
	adjWisdom = IntegerField('adjWis', validators=[ Optional() ])
	adjCharisma = IntegerField('adjCha', validators=[ Optional() ])
	# Ability Checks
	adjAbiCheck = IntegerField('adjAbiCheck', validators=[ Optional() ])
	adjStrCheck = IntegerField('adjStrCheck', validators=[ Optional() ])
	adjDexCheck = IntegerField('adjDexCheck', validators=[ Optional() ])
	adjConCheck = IntegerField('adjConCheck', validators=[ Optional() ])
	adjIntCheck = IntegerField('adjIntCheck', validators=[ Optional() ])
	adjWisCheck = IntegerField('adjWisCheck', validators=[ Optional() ])
	adjChaCheck = IntegerField('adjChaCheck', validators=[ Optional() ])
	# Attacks
	adjAttack = IntegerField('adjAttack', validators=[ Optional() ])
	adjMelee = IntegerField('adjMelee', validators=[ Optional() ])
	adjRanged = IntegerField('adjRanged', validators=[ Optional() ])
	adjCMB = IntegerField('adjCMB', validators=[ Optional() ])
	# Defenses
	adjDef = IntegerField('adjDef', validators=[ Optional() ])
	adjAC = IntegerField('adjAC', validators=[ Optional() ])
	adjCMD = IntegerField('adjCMD', validators=[ Optional() ])
	flatfooted = BooleanField('flatfooted', validators=[ Optional() ])
	# Saves
	adjSaves = IntegerField('adjSaves', validators=[ Optional() ])
	adjFort = IntegerField('adjFort', validators=[ Optional() ])
	adjRef = IntegerField('adjRef', validators=[ Optional() ])
	adjWill = IntegerField('adjWill', validators=[ Optional() ])
	# Skills
	adjSkills = IntegerField('adjSkills', validators=[ Optional() ])
	# Miscellaneous
	adjInit = IntegerField('adjInit', validators=[ Optional() ])
	adjSpeed = IntegerField('adjSpeed', validators=[ Optional() ])
