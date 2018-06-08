from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    characters = db.relationship('Character', backref='player', lazy='dynamic')

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

class Character(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	file = db.Column(db.String(200), unique=True)
	image = db.Column(db.String(200))
	race = db.Column(db.String(32))
	classes = db.Column(db.String(64))
	level = db.Column(db.Integer)
	player_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	notes = db.relationship('Note', backref='character', lazy='dynamic')
	
	def get_id(self):
		try:
			return unicode(self.id) # python 2
		except NameError:
			return str(self.id) # python 3
			
	def __repr__(self):
		return '<Character %r>' % (self.name)
		
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    scratchpad = db.Column(db.Boolean, default=False)
	
    def get_id(self):
        try:
            return unicode(self.id) # python 2
        except NameError:
            return str(self.id) # python 3
			
    def __repr__(self):
        return '<Note %r>' % (self.title)

class Adjustment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	category = db.Column(db.String(64), index=True, unique=True)
	description = db.Column(db.Text)
	# Ability Scores
	adjStrength = db.Column(db.Integer)
	adjDexterity = db.Column(db.Integer)
	adjConstitution = db.Column(db.Integer)
	adjIntelligence = db.Column(db.Integer)
	adjWisdom = db.Column(db.Integer)
	adjCharisma = db.Column(db.Integer)
	# Ability Checks
	adjAbiCheck = db.Column(db.Integer)
	adjStrCheck = db.Column(db.Integer)
	adjDexCheck = db.Column(db.Integer)
	adjConCheck = db.Column(db.Integer)
	adjIntCheck = db.Column(db.Integer)
	adjWisCheck = db.Column(db.Integer)
	adjChaCheck = db.Column(db.Integer)
	# Attacks
	adjAttack = db.Column(db.Integer)
	adjMelee = db.Column(db.Integer)
	adjRanged = db.Column(db.Integer)
	adjCMB = db.Column(db.Integer)
	# Defenses
	adjDef = db.Column(db.Integer)
	adjAC = db.Column(db.Integer)
	adjCMD = db.Column(db.Integer)
	flatfooted = db.Column(db.Boolean)
	# Saves
	adjSaves = db.Column(db.Integer)
	adjFort = db.Column(db.Integer)
	adjRef = db.Column(db.Integer)
	adjWill = db.Column(db.Integer)
	# Skills
	adjSkills = db.Column(db.Integer)
	# Miscellaneous
	adjInit = db.Column(db.Integer)
	adjSpeed = db.Column(db.Integer)
	
	def get_id(self):
		try:
			return unicode(self.id) # python 2
		except NameError:
			return str(self.id) # python 3
			
	def __repr__(self):
		return '<Adjustment %r>' % (self.name)