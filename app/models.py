from app import db, files, images
# from PIL import Image, ImageFilter
from user import UserBase
import collections, datetime, json, os, re, uuid, xmltodict

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(UserBase):
    characters = db.relationship('Character', backref='player', lazy='dynamic')

class Character(Base):
    name = db.Column(db.String(64), index=True, unique=True)
    file = db.Column(db.String(200), unique=True)
    image = db.Column(db.String(200))
    race = db.Column(db.String(32))
    classes = db.Column(db.String(64))
    level = db.Column(db.Integer)
    player_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    notes = db.relationship('Note', backref='character', lazy='dynamic')

    def __init__(self, player, xml, image):
        self.player_id = player.id
        self.save_files(xml, image)

    def update(self):
        character = self.character_data()
        self.name = character['@name']
        self.race = character['race']['@name']
        self.classes = character['classes']['@summaryabbr']
        self.level = character['classes']['@level']
        self.save()

    def save_files(self, xml, image):
        if not image and not self.image:
            return

        if not xml and not self.file:
            return

        filename = str(uuid.uuid4().hex)

        if image:
            image_file = images.save(image, name=filename + '.')
            # Delete the old files, save the new
            if self.image:
                os.remove(images.path(self.image))
            self.image = image_file
            #self.squarePortrait();

        if xml:
            xml_file = files.save(xml, name=filename + '.')
            if self.file:
                os.remove(files.path(self.file))
            self.file = xml_file
            self.update()

        self.save()

    def squarePortrait(self):
        path = images.path(self.portrait)
        image = Image.open(path)

        if image.size[0] < image.size[1]:
            side = image.size[0]
        else:
            side = image.size[1]

        # If the offset would be uneven, remove 1 more pixel
        if (image.size[0] - side) % 2 != 0:
            side -= 1
        offset = (image.size[0] - side) // 2
        box = (offset, 0, offset + side, side)

        image = image.crop(box)
        image.save(path, format='PNG', quality=100)

    def file_url(self):
        return files.url(self.file)

    def image_url(self):
        return images.url(self.image)

    def character_data(self):
        with open(files.path(self.file)) as fd:
            rawdata = xmltodict.parse(fd.read())
        return rawdata['document']['public']['character']

    def delete(self):
        if self.image:
            os.remove(images.path(self.image))
        if self.file:
            os.remove(files.path(self.file))
        super(Character, self).delete()

	def __repr__(self):
		return '<Character %r>' % (self.name)

class Note(Base):
    title = db.Column(db.String(64))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    body = db.Column(db.Text)
    scratchpad = db.Column(db.Boolean, default=False)

    def __init__(self, character):
        self.title = ""
        self.character_id = character.id
        self.body = ""
        self.save()

    def __repr__(self):
        return '<Note %r>' % (self.title)

class Adjustment(Base):
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

    def __init__(self, name, category, description):
        self.name = name
        self.category = category
        self.description = description
        self.save()

    def __repr__(self):
        return '<Adjustment %r>' % (self.name)
