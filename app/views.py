from flask import render_template, flash, jsonify, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
from werkzeug import secure_filename
from app import app, db, lm, models
from .forms import LoginForm, CharacterForm, AdjustmentForm
from .models import Adjustment, Character, Note, User
from operator import itemgetter
import __builtin__, collections, json, re, os, xmltodict

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
@login_required
def index():
    users = models.User.query.all()
    user = g.user

    return render_template('index.html', title="Home", users=users, user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user.get_id() is not None:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username, password=password).first()
        if user is None:
            flash ('Username or password is invalid' , 'error')
            return redirect(url_for('login'))
        login_user(user)
        flash('Logged in successfully!')
	#session['remember_me'] = form.remember_me.data
        return redirect(url_for('user', userid=user.username))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/<userid>')
@login_required
def user(userid):
    user = g.user
    data = {}

    if user == None:
        flash('User %s not found.' % userid)
        return redirect(url_for('index'))

    data['characters'] = models.Character.query.order_by(Character.name)

    return render_template('user.html', title='Characters', user=user, data=data)

def character_filetype(filename):
    return "." in filename and filename.rsplit('.', 1)[1] == 'xml'
	
# Adjustments for the character sheet - conditions, combat mods, etc.
@app.route('/adjustments', methods=['GET', 'POST'])
@login_required
def adjustments():
	user = g.user
	page = 'adjustments'
	title = 'Adjustments'
	adjustments = models.Adjustment.query.order_by(Adjustment.name)
						
	return render_template('adjustments.html', user=user, page=page, title=title, adjustments=adjustments)
	
# Adjustments for the character sheet - conditions, combat mods, etc.
@app.route('/adjustments/new', methods=['GET', 'POST'])
@login_required
def adjustment_new():
	user = g.user
	page = 'adjustments'
	adjustments = models.Adjustment.query.order_by(Adjustment.name)
	form = AdjustmentForm()
	if form.validate_on_submit():
		adjustment = Adjustment(name=form.name.data, category=form.category.data, 
						description=form.description.data, adjStrength=form.adjStrength.data, 
						adjDexterity=form.adjDexterity.data, adjConstitution=form.adjConstitution.data, 
						adjIntelligence=form.adjIntelligence.data, adjWisdom=form.adjWisdom.data, 
						adjCharisma=form.adjCharisma.data, adjAbiCheck=form.adjAbiCheck.data, 
						adjStrCheck=form.adjStrCheck.data, adjDexCheck=form.adjDexCheck.data, 
						adjConCheck=form.adjConCheck.data, adjIntCheck=form.adjIntCheck.data, 
						adjWisCheck=form.adjWisCheck.data, adjChaCheck=form.adjChaCheck.data, 
						adjAttack=form.adjAttack.data, adjMelee=form.adjMelee.data, adjRanged=form.adjRanged.data, 
						adjCMB=form.adjCMB.data, adjDef=form.adjDef.data, adjAC=form.adjAC.data, 
						adjCMD=form.adjCMD.data, flatfooted=form.flatfooted.data, adjSaves=form.adjSaves.data, 
						adjFort=form.adjFort.data, adjRef=form.adjRef.data, adjWill=form.adjWill.data, 
						adjSkills=form.adjSkills.data, adjInit=form.adjInit.data, adjSpeed=form.adjSpeed.data) 
		db.session.add(adjustment)
		db.session.commit()
		return redirect(url_for('adjustments'))
						
	return render_template('edit-adjustment.html', user=user, title="New Adjustment", 
							adjustments=adjustments, form=form)

# Adjustments for the character sheet - conditions, combat mods, etc.
@app.route('/adjustments/<name>', methods=['GET', 'POST'])
@login_required
def adjustment_edit(name):
	user = g.user
	page = 'adjustments'
	adjustment = Adjustment.query.filter_by(name=name).first()
	adjustments = models.Adjustment.query.order_by(Adjustment.name)
	form = AdjustmentForm(obj=adjustment)
	if form.validate_on_submit():
		adjustment.name = form.name.data
		adjustment.category = form.category.data
		adjustment.description = form.description.data
		adjustment.adjStrength = form.adjStrength.data
		adjustment.adjDexterity = form.adjDexterity.data
		adjustment.adjConstitution = form.adjConstitution.data
		adjustment.adjIntelligence = form.adjIntelligence.data
		adjustment.adjWisdom = form.adjWisdom.data
		adjustment.adjCharisma = form.adjCharisma.data
		adjustment.adjAbiCheck = form.adjAbiCheck.data
		adjustment.adjStrCheck = form.adjStrCheck.data
		adjustment.adjDexCheck = form.adjDexCheck.data
		adjustment.adjConCheck = form.adjConCheck.data
		adjustment.adjIntCheck = form.adjIntCheck.data
		adjustment.adjWisCheck = form.adjWisCheck.data
		adjustment.adjChaCheck = form.adjChaCheck.data
		adjustment.adjAttack = form.adjAttack.data
		adjustment.adjMelee = form.adjMelee.data
		adjustment.adjRanged = form.adjRanged.data
		adjustment.adjCMB = form.adjCMB.data
		adjustment.adjDef = form.adjDef.data
		adjustment.adjAC = form.adjAC.data
		adjustment.adjCMD = form.adjCMD.data
		adjustment.flatfooted = form.flatfooted.data
		adjustment.adjSaves = form.adjSaves.data
		adjustment.adjFort = form.adjFort.data
		adjustment.adjRef = form.adjRef.data
		adjustment.adjWill = form.adjWill.data
		adjustment.adjSkills = form.adjSkills.data
		adjustment.adjInit = form.adjInit.data
		adjustment.adjSpeed = form.adjSpeed.data
		#Commit changes
		db.session.add(adjustment)
		db.session.commit()
		return redirect(url_for('adjustments'))
	
	form.name.data = adjustment.name
	form.category.data = adjustment.category
	form.description.data = adjustment.description
	form.adjStrength.data = adjustment.adjStrength
	form.adjDexterity.data = adjustment.adjDexterity
	form.adjConstitution.data = adjustment.adjConstitution 
	form.adjIntelligence.data = adjustment.adjIntelligence
	form.adjWisdom.data = adjustment.adjWisdom
	form.adjCharisma.data = adjustment.adjCharisma
	form.adjAbiCheck.data = adjustment.adjAbiCheck
	form.adjStrCheck.data = adjustment.adjStrCheck
	form.adjDexCheck.data = adjustment.adjDexCheck
	form.adjConCheck.data = adjustment.adjConCheck
	form.adjIntCheck.data = adjustment.adjIntCheck
	form.adjWisCheck.data = adjustment.adjWisCheck
	form.adjChaCheck.data = adjustment.adjChaCheck
	form.adjAttack.data = adjustment.adjAttack
	form.adjMelee.data = adjustment.adjMelee
	form.adjRanged.data = adjustment.adjRanged
	form.adjCMB.data = adjustment.adjCMB
	form.adjDef.data = adjustment.adjDef
	form.adjAC.data = adjustment.adjAC
	form.adjCMD.data = adjustment.adjCMD
	form.adjSaves.data = adjustment.adjSaves
	form.adjFort.data = adjustment.adjFort
	form.adjRef.data = adjustment.adjRef
	form.adjWill.data = adjustment.adjWill
	form.adjSkills.data = adjustment.adjSkills
	form.adjInit.data = adjustment.adjInit
	form.adjSpeed.data = adjustment.adjSpeed
		
	return render_template('edit-adjustment.html', user=user, title="Edit Adjustment", 
							adjustments=adjustments, form=form)
	
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    user = g.user
    form = CharacterForm("")
    if form.validate_on_submit():
        # Check if the user has a direct, and if not, create one
        userdirectory = os.path.join('/home/kitka/src/charsheetPF/app/static/uploads', user.username)
        if not os.path.isdir( userdirectory ):
            os.makedirs( userdirectory )
        # XML File
        filename = secure_filename( form.xml_file.data.filename )
        filepath = os.path.join(userdirectory, filename)
        file_data = request.files[form.xml_file.name].read()
        open(filepath, 'w').write(file_data)
        # Image File
        if not form.image_file.data:
            image = '/static/images/thumb.jpg'
        else:
            image_filename = filename.split('.')[0] + '.' + form.image_file.data.filename.split('.')[-1]
            imagepath = os.path.join(userdirectory, image_filename)
            image_data = request.files[form.image_file.name].read()
            open(imagepath, 'w').write(image_data)
            image = os.path.join('/static/uploads', user.username, image_filename)
        # Read file to extract goodies
        rawdata = xmltodict.parse(file_data)
        character = rawdata['document']['public']['character']
        char_data = Character(name = character['@name'], file = filepath, 
                        image = image, race = character['race']['@name'], 
                        classes = character['classes']['@summaryabbr'], 
                        level = character['classes']['@level'])
        db.session.add(char_data)
        db.session.commit()
        new_character = Character.query.filter_by(name=character['@name']).first()
        note = Note(title="Scratch Pad", body="", scratchpad=True, character_id=new_character.id, timestamp=datetime.utcnow())
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('character', userid=user.username, id=char_data.id))
    return render_template('upload.html', title='Upload New Character', user=user, form=form)
	
@app.route('/<userid>/character/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_char(userid, id):
    user = g.user
    char_data = Character.query.filter_by(id=id).first()
    file_nameonly = char_data.file.split('/')[-1]
    form = CharacterForm(file_nameonly, obj=char_data)
    if form.validate_on_submit():
        userdirectory = os.path.join('/home/kitka/src/charsheetPF/app/static/uploads', user.username)
        # XML File
        if form.xml_file.data:
            filename = secure_filename( form.xml_file.data.filename )
            filepath = os.path.join(userdirectory, filename)
            file_data = request.files[form.xml_file.name].read()
            open(filepath, 'w').write(file_data)
            # Read file to extract goodies
            rawdata = xmltodict.parse(file_data)
            character = rawdata['document']['public']['character']
            char_data.name = character['@name']
            char_data.race = character['race']['@name'] 
            char_data.classes = character['classes']['@summaryabbr']
            char_data.level = character['classes']['@level']
            char_data.file = filepath
        # Image File
        if form.image_file.data:
            image_filetype = form.image_file.data.filename.split('.')[-1]
            if not form.xml_file.data:
                image_filename = ( char_data.file.split('/')[-1] ).split('.')[0] + '.' + image_filetype
            else:
                image_filename = filename.split('.')[0] + '.' + image_filetype
            imagepath = os.path.join(userdirectory, image_filename) 
            image_data = request.files[form.image_file.name].read()
            open(imagepath, 'w').write(image_data)
            char_data.image = os.path.join('/static/uploads', user.username, image_filename)
        db.session.add(char_data)
        db.session.commit()
        return redirect(url_for('character', userid=user.username, id=char_data.id))
    return render_template('upload.html', title='Update ' + char_data.name, 
                            form=form, user=user, character=char_data)

@app.route('/<userid>/character/<id>/delete', methods=['GET', 'DELETE'])
@login_required
def delete_character(userid, id):
	user = g.user
	character = Character.query.filter_by(id=id).first()
	if character is not None:
		os.remove( character.file )
		os.remove( "/home/kitka/src/charsheetPF/app" + character.image )
		db.session.delete(character)
		db.session.commit()
		return redirect(url_for('user', userid=user.username))
	
@app.route('/note/autosave/', methods=['POST'])
@login_required
def autosave_note():
    user = g.user
    note = Note.query.filter_by(id=request.json['id']).first()
    note.title = request.json['title']
    note.body = request.json['body']
    note.timestamp = datetime.utcnow()
    db.session.add(note)
    db.session.commit()
    return jsonify( { 'message' : 'Success!', 'id' : note.id, 'title' : note.title, 
                      'body' : note.body, 'timestamp' : note.timestamp } )
    
@app.route('/note/new/', methods=['POST'])
@login_required
def new_note():
    user = g.user
    note = Note(title=request.json['title'], body=request.json['body'], scratchpad=False, timestamp=datetime.utcnow(), character_id=request.json['character'])
    db.session.add(note)
    db.session.commit()
    return jsonify( { 'id' : note.id, 'title' : note.title, 'body' : "" } )
    
@app.route('/note/delete/', methods=['POST'])
@login_required
def delete_note():
    user = g.user
    note = Note.query.filter_by(id=request.json['id']).first()
    if not note.scratchpad:
        db.session.delete(note)
        db.session.commit()
        message = "Success!"
    else:
        message = "You can't delete that!"
    return jsonify( { 'message' : message, 'id' : request.json['id'] } )
    
@app.template_global(name='zip') 
def _zip(*args, **kwargs): #to not overwrite builtin zip in globals
	return __builtin__.zip(*args, **kwargs)

@app.template_filter()
def mergelists(list1, *args):
    if not list1:
        oldlist = []
    elif type(list1) != type([]):
		oldlist = [list1]
    else:
		oldlist = list1
    newlist = oldlist
    for x in args:
        if type(x) == type([]):
            newlist = filter(None, newlist + x)
        elif type(x) == type(collections.OrderedDict( [] )):
            listx = [x]
            newlist = filter(None, newlist + listx)
    newlist = sorted(newlist, key=itemgetter('@name'))
    return newlist
    
@app.template_filter()
def makelist(list, *args):
    if not list:
        return []
    elif type(list) != type([]):
        return [list]
    else:
        return list
	
@app.template_filter()
def removefromlist(list1, *args):
    if list1:
        if type(list1) != type([]):
            list1 = [list1]
        list2 = []
        for i in args:
            if type(i) == type(collections.OrderedDict( [] )):
                list2 = list2 + [i]
            elif type(i) == type([]):
                list2 = list2 + i
        check = [ y['@name'] for y in list2 ]
        newlist = [x for x in list1 if ( x['@name'] not in check) ]
        return newlist
    return []
	
@app.template_filter()
def getdescription(ability, *args):
	specialList = []
	for i in args:
		if i and type(i) == type(collections.OrderedDict( [] )):
			specialList = specialList + [i]
		elif i and type(i) == type([]):
			specialList = specialList + i
	for special in specialList:
		if special['@name'] == ability:
			return special['description']
	return "Description."

@app.template_filter()
def getbyname(list, name):
	if type(list) == type(collections.OrderedDict( [] )):
		checklist = [list]
	else:
		checklist = list
	for x in checklist:
		if x['@name'] == name:
			return x
	
def filterspells(spells, sp_lv, sp_class):
	filtered = [x for x in spells if ( x['@level'] == sp_lv and x['@class'] == sp_class) ]
	return filtered
	
@app.template_filter()
def paragrapher(value):
    if not value:
        return '<p></p>'
    else:
        return '<p>' + '</p><p>'.join( [s.strip() for s in value.splitlines()] ) + '</p>'

@app.route('/<userid>/character/<id>')
@login_required
def character(userid, id):
    character_saved = Character.query.filter_by(id=id).first()
    user = g.user
    image = character_saved.image
    saved_adjustments = Adjustment.query.order_by(Adjustment.name)
    with open( character_saved.file ) as fd:
        rawdata = xmltodict.parse(fd.read())
    character = rawdata['document']['public']['character']
	
    xp_charts = {}
    xp_charts['slow'] = [0, 3000, 7500, 14000, 23000, 35000, 53000, 77000, 115000, 160000, 235000, 330000, 475000, 665000, 955000, 1350000, 1900000, 2700000, 3850000, 5350000]
    xp_charts['medium'] = [0, 2000, 5000, 9000, 15000, 23000, 35000, 51000, 75000, 105000, 155000, 220000, 315000, 445000, 635000, 890000, 1300000, 1800000, 2550000, 3600000]
    xp_charts['fast'] = [0, 1300, 3300, 6000, 10000, 15000, 23000, 34000, 50000, 71000, 105000, 145000, 210000, 295000, 425000, 600000, 850000, 1200000, 1700000, 2400000]
	
    if not character['melee']:
		character['melee'] = { 'weapon' : '' }
    if not character['ranged']:
		character['ranged'] = { 'weapon' : '' }
		
    if character['magicitems']['item']:
        magic_items = {}
        magic_items['consumables'] = [ i for i in character['magicitems']['item'] if ( i['@name'].startswith('Potion') or i['@name'].startswith('Scroll') or i['@name'].startswith('Wand') or i['@name'].startswith('Oil of') ) ]
        magic_items['normal'] = removefromlist( character['magicitems']['item'], character['melee']['weapon'], character['ranged']['weapon'], character['defenses']['armor'], magic_items['consumables'] )
		
    key_stats = {
        'ac' : int(character['armorclass']['@ac']), 
        'cmd' : int(character['maneuvers']['@cmd']), 
        'initiative' : int(character['initiative']['@total']), 
        'speed' : int(character['movement']['speed']['@value']), 
        'cmb' : int(character['maneuvers']['@cmb']), 
    }
	
    for save in character['saves']['save']:
        key_stats[save['@abbr'] + ' save'] = int(save['@save'])
    for abi in character['attributes']['attribute']:
        key_stats[abi['@name'][:3] + 'score'] = int(abi['attrvalue']['@modified'])
		
    spellLists = {}

    if character['spellclasses']:
        if type(character['spellclasses']['spellclass']) != type([]):
            spellclasses = [character['spellclasses']['spellclass']]
        else:
            spellclasses = character['spellclasses']['spellclass']
        for casting_class in spellclasses:
            spells_by_level = {}
            for spell_lv in range( int(casting_class['@maxspelllevel'])+1 ):
                if casting_class['@spells'] == 'Memorized':
                    spells_by_level[spell_lv] = filterspells( character['spellsmemorized']['spell'], str(spell_lv), casting_class['@name'] )
                elif casting_class['@spells'] == 'Spontaneous':
                    spells_by_level[spell_lv] = filterspells( character['spellsknown']['spell'], str(spell_lv), casting_class['@name'] )
            spellLists[ casting_class['@name'] ] = spells_by_level
	
    scratchpad = character_saved.notes.filter_by(scratchpad=True).first()
    notes = character_saved.notes.filter_by(scratchpad=False).order_by(Note.title)
    
    return render_template('/character/character.html', user=user, 
            advancement=xp_charts, key_stats=key_stats, spellLists=spellLists, 
            image=image, saved_adjustments=saved_adjustments, id=id, 
            magic_items=magic_items, character=character, scratchpad=scratchpad, 
            notes=notes)