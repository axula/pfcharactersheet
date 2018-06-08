from flask import g
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask.ext.uploads import UploadSet, IMAGES
from app.models import Character
import os

images = UploadSet('images', IMAGES)

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default = False)

class CharacterForm(Form):
	xml_file = FileField('xml_file', validators=[ FileAllowed(['xml']) ])
	image_file = FileField('image_file', validators=[ FileAllowed(images, 'Images only!') ])
	
	def __init__(self, stored_file, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.stored_file = stored_file
	
	def validate(self):
		filename = os.path.join('/home/kitka/src/charsheetPF/app/static/uploads', g.user.username, self.xml_file.data.filename)
		if self.stored_file:
			if self.xml_file.data.filename == self.stored_file:
				return True
		else:
			if not self.xml_file.data:
				return False
		character_file = Character.query.filter_by(file=filename).first()
		if character_file != None:
			self.xml_file.errors.append('A file by this name already exists.')
			return False
		return True

class AdjustmentForm(Form):
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