from flask import render_template, flash, jsonify, redirect, session, url_for, request, g
from app import app, db, files, images, lm
from user import views
from flask_login import login_required
from datetime import datetime
from werkzeug import secure_filename
from .forms import *
from .models import *
from operator import itemgetter
import __builtin__, collections, json, re, os, xmltodict

@app.route('/')
@app.route('/index')
@login_required
def index():
    users = User.query.all()
    user = g.user

    return render_template('index.html', title="Home", users=users, user=user)

@app.route('/characters')
@login_required
def characters():
    user = g.user
    data = {}

    data['characters'] = user.characters
    for char in data['characters']:
        print images.url(char.image)

    return render_template('characters.html', title='Characters', user=user, data=data)

def character_filetype(filename):
    return "." in filename and filename.rsplit('.', 1)[1] == 'xml'

# Adjustments for the character sheet - conditions, combat mods, etc.
@app.route('/adjustments', methods=['GET', 'POST'])
@login_required
def adjustments():
	user = g.user
	page = 'adjustments'
	adjustments = Adjustment.query.order_by(Adjustment.name)

	return render_template('adjustments.html', user=user, page=page, title='Adjustments', adjustments=adjustments)

# Adjustments for the character sheet - conditions, combat mods, etc.
@app.route('/adjustments/new', methods=['GET', 'POST'])
@login_required
def adjustment_new():
	user = g.user
	page = 'adjustments'
	adjustments = Adjustment.query.order_by(Adjustment.name)
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
@app.route('/adjustments/<id>', methods=['GET', 'POST'])
@login_required
def adjustment_edit(id):
	user = g.user
	page = 'adjustments'
	adjustment = Adjustment.query.get(id)
	adjustments = Adjustment.query.order_by(Adjustment.name)
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
    form = CharacterForm()
    if form.validate_on_submit():
        char = Character(user, form.xml_file.data, form.image_file.data)

        note = Note(char)
        note.title = "Scratch Pad"
        note.scratchpad = True
        note.save()

        return redirect(url_for('character', id=char.id))
    return render_template('upload.html', title='Upload New Character', user=user, form=form)

@app.route('/character/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_char(id):
    user = g.user
    character = Character.query.get(id)

    if character is None or user.id != character.player_id:
        return redirect(url_for('characters'))

    form = EditCharacterForm(obj=character)

    if form.validate_on_submit():
        if form.xml_file.data or form.image_file.data:
            character.save_files(form.xml_file.data, form.image_file.data)

        return redirect(url_for('character', userid=user.username, id=character.id))
    return render_template('upload.html', title='Update ' + character.name,
                            form=form, user=user, character=character)

@app.route('/character/<id>/delete', methods=['GET', 'DELETE'])
@login_required
def delete_character(id):
    user = g.user
    character = Character.query.get(id)

    if character is not None and user.id == character.player_id:
        character.delete()

    return redirect(url_for('characters'))

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

@app.route('/character/<id>')
@login_required
def character(id):
    user = g.user
    character_saved = Character.query.get(id)

    if character_saved is None or user.id != character_saved.player_id:
        return redirect(url_for('characters'))

    character = character_saved.character_data()
    character.image = character_saved.image_url()

    xp_charts = {
        'slow'   : [0, 3000, 7500, 14000, 23000, 35000, 53000, 77000, 115000, 160000, 235000,
                    330000, 475000, 665000, 955000, 1350000, 1900000, 2700000, 3850000, 5350000],
        'medium' : [0, 2000, 5000, 9000, 15000, 23000, 35000, 51000, 75000, 105000, 155000,
                    220000, 315000, 445000, 635000, 890000, 1300000, 1800000, 2550000, 3600000],
        'fast'   : [0, 1300, 3300, 6000, 10000, 15000, 23000, 34000, 50000, 71000, 105000,
                    145000, 210000, 295000, 425000, 600000, 850000, 1200000, 1700000, 2400000],
    }

    if not character['melee']:
		character['melee'] = { 'weapon' : '' }
    if not character['ranged']:
		character['ranged'] = { 'weapon' : '' }

    if character['magicitems']['item']:
        magic_items = {}
        magic_items['consumables'] = [ i for i in character['magicitems']['item'] if ( i['@name'].startswith('Potion') or i['@name'].startswith('Scroll') or i['@name'].startswith('Wand') or i['@name'].startswith('Oil of') ) ]
        magic_items['normal'] = removefromlist( character['magicitems']['item'], character['melee']['weapon'], character['ranged']['weapon'], character['defenses']['armor'], magic_items['consumables'] )

    key_stats = {
        'name' : character['@name'],
        'race' : character['race']['@name'],
        'classes' : re.sub(r'\([^)]*\)', '', character['classes']['@summary']),
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

    return render_template('/character/character.html', user=user, advancement=xp_charts,
                           key_stats=key_stats, spellLists=spellLists, magic_items=magic_items,
                           character=character, scratchpad=scratchpad, notes=notes)
