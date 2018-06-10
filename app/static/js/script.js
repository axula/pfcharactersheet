/* Admin Pages */

$('#new').on('shown.bs.modal', function () {
  $('#myInput').focus()
})

// Upload Image Preview
$('#image_file').change( function () {
    var reader = new FileReader();

    reader.onload = function (e) {
        // get loaded data and render thumbnail
        $('#image-preview img').attr('src', e.target.result);
    };

    // read the image file as a data URL
    reader.readAsDataURL(this.files[0]);
});

/* Character Sheet */

$(document).ready(function () {
    $("td").tooltip({container:'body'});
    $("dd").tooltip({container:'body'});
    $("span").tooltip({container:'body'});
    $("h5").tooltip({container:'body'});
    $("h6").tooltip({container:'body'});

    var overlay_height = $(window).height() - 32 - 85;
    $('.popup-content').height(overlay_height);

    var content_height = $(window).height() - 50 - 15;
    $('.content').height(content_height);

    var minion_height = $('.popup-content').height() - 64 - 15;
    $('.minion-content').height(minion_height);

    if ( localStorage.getItem('notes') !== null) {
        var notes = JSON.parse( localStorage.getItem('notes'));
        $.each( notes, function( key, note ) {
            // { id, title, body, timestamp }
            // If the note is only in localStorage, save it to the database
            if (note.id === "") {
                var data = { title : note.title, body : note.body,
                             character : parseInt( $('#character-name h1').data('id') ) };
                $.ajax({
                    type: "POST",
                    url: "/note/new/",
                    contentType: "application/json; charset=utf-8",
                    data: JSON.stringify(data, null, '\t'),
                    success: function(data) {
                        $('#notes-list').append(
                            '<li><a href="#" data-id="' + data.id + '" data-body="">' + data.title + '</a></li>' );
                        var index = notes.indexOf(note);
                        notes[index].id = data.id
                        console.log(notes[index]);
                        console.log(notes[index].title);
                        localStorage.setItem( 'notes', JSON.stringify(notes) );
                    }
                });
            }
            var note_listing = $('#note-' + note.id + ' a');
            var timestamp = Date.parse(note_listing.data('timestamp'));
            // If the local stroage data is newer that the data from the server
            if (note.timestamp > timestamp) {
                var data = { id : parseInt( note.id ),
                             title : note.title,
                             body : note.body }
                $.ajax({
                    type: "POST",
                    url: "/note/autosave/",
                    contentType: "application/json; charset=utf-8",
                    data: JSON.stringify(data, null, '\t'),
                    success: function(data) {
                        $(note_listing).text(note.title);
                        $(note_listing).data('body', note.body);
                        $(note_listing).data('timestamp', note.timestamp)
                        // If it's the active element, update the current view
                        if ( note_listing.parent().hasClass('scratchpad') ) {
                            $('#note-title').text(note.title);
                            $('.note-body').text(note.body);
                        }
                    }
                });
            }
        });
    }
    localStorage.setItem( 'notes', JSON.stringify([]) );
});

$(window).resize(function() {
    var overlay_height = $(window).height() - 32 - 85;
    $('.popup-content').height(overlay_height);

    var content_height = $(window).height() - 50 - 15;
    $('.content').height(content_height);

    var minion_height = $('.popup-content').height() - 64 - 15;
    $('.minion-content').height(minion_height);

    $('#notes .nav-pills').height( $(window).height() - 149 - 32 - 10 );
    $('.note-body').height( $(window).height() - 149 - 32 - 10 - 43 );
});

$(function () {
  $('[data-toggle="popover"]').popover()
})

$('#weapon-options').collapse({
	toggle: false
})

$('.abilities-collapse').collapse({
	toggle: false
})

$('#adjustmentMenu').on('show.bs.modal', function () {
	$('#adjustmentMenuBody').css('height',$( window ).height()*0.9);
	$('#adjustment-list').css('height',$('#adjustmentMenuBody').height()-200);
	$('#adj-description').css('height',$('#adjustmentMenuBody').height()-161);
});

$('#page-nav a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})

/* Footer Nav */

$('#link-notes').click(function () {
    if ( $('#game-adjustments').css('display') == 'none' && $('.minion-sheet').css('display') == 'none' ) {
        $('#notes').toggle();
        $('.popup-overlay').toggle();
    } else {
        $('.popup-overlay').show();
        $('.minion-sheet').hide();
        $('#game-adjustments').hide();
        $('#notes').show();
    }

    $('#notes .nav-pills').height( $(window).height() - 149 - 32 - 10 );
    $('.note-body').height( $(window).height() - 149 - 32 - 10 - 43 );
});

$('#link-adjustments').click(function () {
    if ( $('#notes').css('display') == 'none' && $('.minion-sheet').css('display') == 'none' ) {
        $('#game-adjustments').toggle();
        $('.popup-overlay').toggle();
    } else {
        $('.popup-overlay').show();
        $('#notes').hide();
        $('.minion-sheet').hide();
        $('#game-adjustments').show();
    }
});

$('.minion-link').click(function () {
    var name = $(this).attr('id').replace('link-', '');
    if ( $('#notes').css('display') == 'none' && $('#game-adjustments').css('display') == 'none' ) {
        $('#' + name).toggle();
        $('.popup-overlay').toggle();
    } else {
        $('.popup-overlay').show();
        $('#notes').hide();
        $('#game-adjustments').hide();
        $('#' + name).show();
    }
});

/* Notes */

$(document).on('click', '#notes .nav-pills li a', function(e) {
    e.preventDefault();
    $('#notes-list .active').removeClass('active');
    if ( !$(this).parent().hasClass('scratchpad') ) {
        $(this).parent().addClass('active');
        $('#note-title').attr('contenteditable', true);
        $('#note-options').show();
    } else {
        $('#note-title').attr('contenteditable', false);
        $('#note-options').hide();
    }
    $('#note-title').data( 'id', $(this).data('id') );
    console.log( $('#note-title').data( 'id') );
    $('#note-title').text( $.trim( $(this).text() ) );
    $('.note-body').text( $(this).data('body') );
});

$('.note-editable').blur(function() {
    var data = { id : parseInt( $('#note-title').data('id') ),
                 title : $.trim( $('#note-title').text() ),
                 body : $('.note-body').text() };
    $.ajax({
        type: "POST",
        url: "/note/autosave/",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data, null, '\t'),
        success: function(data) {
            if ( !$('#note-' + data.id).hasClass('scratchpad') ) {
                $('#note-' + data.id + ' a').text( data.title );
            }
            $('#note-' + data.id + ' a').data('body', data.body);
        },
        error: function() {
            // save to local storagenote = {}
            var notes = JSON.parse( localStorage.getItem('notes'));
            var id = parseInt( $('#note-title').data('id') )
            // Update the existing data if the key exists
            var note = $.grep(notes, function(e){ return e.id == id; })[0];
            var index = notes.indexOf(note);
            if( index === -1 ) {
                // Otherwise, create a new dictionary and add it to the array
                note = {};
                note.id = id;
                note.title = $('#note-title').text();
                note.body = $.trim( $('.note-body').text() );
                note.timestamp = Date.now();
                notes.push(note);
                if ( !$('#note-' + note.id).hasClass('scratchpad') ) {
                    $('#note-' + note.id + ' a').text( note.title );
                }
                $('#note-' + note.id + ' a').data('body', note.body);
            } else {
                notes[index].id = id;
                notes[index].title = $('#note-title').text();
                notes[index].body = $.trim( $('.note-body').text() );
                notes[index].timestamp = Date.now();
                if ( !$('#note-' + note[index].id).hasClass('scratchpad') ) {
                    $('#note-' + notes[index].id + ' a').text( notes[index].title );
                }
                $('#note-' + notes[index].id + ' a').data('body', notes[index].body);
            }
            localStorage.setItem( 'notes', JSON.stringify(notes) );
        }
    });
});

$('#new-note').click(function(e) {
    e.preventDefault();
    var data = { title : "New Note",
                 body : "",
                 character : parseInt( $('#character-name h1').data('id') ) };

    $.ajax({
        type: "POST",
        url: "/note/new/",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data, null, '\t'),
        success: function(data) {
            $('#notes-list .active').removeClass('active');
            $('#notes-list').append(
                '<li id="note-' + data.id + '" class="active"><a href="#" data-id="' + data.id + '" data-body="' + data.body + '">' + data.title + '</a></li>' );
            $('#note-title').data( 'id', data.id );
            console.log( $('#note-title').data( 'id') );
            $('#note-title').text(data.title);
            $('.note-body').text(data.body);
            $('#note-title').attr('contenteditable', true);
            $('#note-options').show();
        },
        error: function() {
            // save to localStorage
            var note = {}
            var notes = JSON.parse( localStorage.getItem('notes'));
            note.id = "";
            note.title = "New Note";
            note.body = "";
            note.timestamp = Date.now();
            notes.push(note);
            localStorage.setItem( 'notes', JSON.stringify(notes) );
            $('#notes-list li').removeClass('active');
            $('#notes-list').append(
                '<li class="active"><a href="#" data-id="' + note.id + '" data-body="' + note.body + '">' + note.title + '</a></li>' );
            $('#note-title').data( 'id', note.id );
            $('#note-title').text(note.title);
            $('.note-body').text(note.body);
            $('#note-title').attr('contenteditable', true);
            $('#note-options').show();
        }
    });
});

$('#note-delete').click(function(e) {
    e.preventDefault;
    var data = { 'id' : parseInt( $('#note-title').data('id') ) }

    $.ajax({
        type: "POST",
        url: "/note/delete/",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data, null, '\t'),
        success: function(data) {
            console.log(data.message);
            var previous = $('#note-' + data.id).prev();
            var id = $(previous.children()[0]).data('id');
            console.log(String(id));
            if ( $('#note-' + id).hasClass('scratchpad') ) {
                $('#note-options').hide();
                $('#note-title').attr('contenteditable', false);
            } else {
                $('#note-options').show();
                $('#note-title').attr('contenteditable', true);
                $('#note-' + id).addClass('active');
            }
            $('#note-title').text( $.trim( $('#note-' + id).text() ) );
            $('#note-title').data( 'id', $('#note-' + id + ' a').data('id') );
            $('.note-body').text( $('#note-' + id + ' a').data( 'body' ) );
            $('#note-' + data.id).remove();
        }
    });
});

function lookup( id, arr ) {
    $.each( arr, function( key, data ) {
        if( data.id === id ) {
            return true;
        }
    });
    return false;
}

$(document).on('keyup', '#search-adj', function() {
    var search = $('#search-adj').val().toLowerCase().trim();
    $('#adjustment-list>li').each(function () {
        var text = $(this).text().toLowerCase().trim();
        (text.indexOf(search) == 0) ? $(this).show() : $(this).hide();
    });
});

/* Daily Reset Functions */

$('#rest-all').click(function (e) {
	e.preventDefault()
	healnum = parseInt( $('#restedHP').attr('title') );
    restedHP(healnum);
    resetTracked();
    resetSpells();
});

$('#restedHP').click(function (e) {
	e.preventDefault()
	healnum = parseInt( $(this).attr('title') );
    restedHP(healnum);
})

$('#restedAbilities').click(function (e) {
	e.preventDefault()
	resetTracked();
})

$('#restedSpells').click(function (e) {
	e.preventDefault()
	resetSpells();
})

function restedHP(healnum) {
	var maxhp = +($('#hp-max').text());
	if (healnum > damagehp) {
		hprecord.unshift( 'Healed ' + damagehp + ' hp' );
		damagehp = 0;
	} else {
		hprecord.unshift( 'Healed ' + healnum + ' hp' );
		damagehp = damagehp - healnum;
	}
	$('#hp-current').text( maxhp - damagehp );
	$('#hp-input').val('');
	displayHPrecord();
}

function resetHP() {
	var maxhp = +($('#hp-max').text())
	damagehp = 0;
	temphp = 0;
	nonlethaldamage = 0;
	$('#hp-current').text( maxhp );
	$('#hp-temp').text('');
	$('#hp-nonlethal').text('');
	$('#hp-temp').text('');
	$('#hp-input').val('');
	hprecord = [];
	displayHPrecord();
}

function resetTracked() {
	$('.daily-ability').each(function(i, obj) {
		var id = $(this).attr('id').replace(/remaininguses/, '');
		var max = $('#maxuses' + id).text();
		$(this).text( max );
	});
}

function resetSpells() {
	$('.spellsremaining').each(function(i, obj) {
		var id = $(this).attr('id').replace(/spellsremaining/, '');
		var max = $('#spellsperday' + id).text();
		$(this).text( max );
	});

	$('.prepared-spellslot').prop('checked', false);
}

/* Tracked Resources */

$('.trackedless').click(function () {
	var id = $(this).attr('id').replace(/trackedless/, '');
	var remaining = $('#remaininguses' + id);
	var num = parseInt( remaining.text() );
	if (num > 0) {
		$(remaining).text( num - 1 );
	}
})

$('.trackedmore').click(function () {
	var id = $(this).attr('id').replace(/trackedmore/, '');
	var remaining = $('#remaininguses' + id);
	var num = parseInt( remaining.text() );
	if (num < parseInt( $('#maxuses' + id).text() ) ) {
		$(remaining).text( num + 1 );
	}
})

$('#tracked-reset').click(function (e) {
	e.preventDefault()
	resetTracked();
})

/* Spells */

$('.slotLess').click(function () {
	var id = $(this).attr('id').replace(/slotLess/, '');
	var remaining = $('#spellsremaining' + id);
	var num = parseInt( remaining.text() );
	if (num > 0) {
		$(remaining).text( num - 1 );
	}
})

$('.slotMore').click(function () {
	var id = $(this).attr('id').replace(/slotMore/, '');
	var remaining = $('#spellsremaining' + id);
	var num = parseInt( remaining.text() );
	if (num < parseInt( $('#spellsperday' + id).text() ) ) {
		$(remaining).text( num + 1 );
	}
})

/* Hit Points */

$('#hp-harm').click(function (e) {
	e.preventDefault()
	var maxhp = +($('#hp-max').text());
	num = +($('#hp-input').val());
	if ( temphp != 0 ) {
		if ( temphp < num ) {
			num = num - temphp;
			temphp = 0;
			$('#hp-temp').text('');
		} else {
			temphp = temphp - num;
			num = 0;
			$('#hp-temp').text( '+' + temphp + ' temp' );
		}
	}
	if ( $('#nonlethal-toggle').is(':checked') ) {  // If damage taken is nonlethal
		nonlethaldamage = nonlethaldamage + num;
		hprecord.unshift( '<span class="hptext-nonlethal">Damaged ' + num + ' hp nonlethal</span>' );
		$('#hp-temp').text( '(' + nonlethaldamage + ' NL dmg)' );
	} else {  // If damage is lethal
		damagehp = damagehp + num;
		hprecord.unshift( '<span class="hptext-damage">Damaged ' + num + ' hp</span>' );
		$('#hp-current').text( maxhp - damagehp );
	}
	$('#hp-input').val('');
	displayHPrecord();
})

$('#hp-heal').click(function (e) {
	e.preventDefault()
	var num = +($('#hp-input').val());
	var maxhp = +($('#hp-max').text());
	if (num > damagehp) {
		hprecord.unshift( '<span class="hptext-heal">Healed ' + damagehp + ' hp</span>' );
		damagehp = 0;
	} else {
		hprecord.unshift( '<span class="hptext-heal">Healed ' + num + ' hp</span>' );
		damagehp = damagehp - num;
	}
	$('#hp-current').text( maxhp - damagehp );
	if (num > nonlethaldamage) {
		hprecord.unshift( '<span class="hptext-heal">Healed ' + nonlethaldamage + ' nonlethal damage</span>' );
		nonlethaldamage = 0;
		$('#hp-temp').text('');
	} else {
		hprecord.unshift( '<span class="hptext-heal">Healed ' + num + ' nonlethal damage</span>' );
		nonlethaldamage = nonlethaldamage - num;
		$('#hp-temp').text( '(' + nonlethaldamage + ' NL dmg)' );
	}
	$('#hp-input').val('');
	displayHPrecord();
})

$('#hp-addtemp').click(function (e) {
	e.preventDefault()
	var num = $('#hp-input').val();
	var hp = $('#hp-current').text();
	hprecord.unshift( '<span class="hptext-temp">Added ' + num + ' temp hp</span>' );
	if ( num > temphp ) {
		$('#hp-temp').text( '+' + num + ' temp' );
		temphp = num;
	}
	$('#hp-input').val('');
	displayHPrecord();
})

$('#hp-reset').click(function (e) {
	e.preventDefault()
	resetHP();
})

$('#hp-undo').click(function (e) {
	e.preventDefault()
	var currenthp = +($('#hp-current').text());
	var maxhp = +($('#hp-max').text());
	if (hprecord[0].indexOf('Damaged') >= 0) {
		var num = hprecord[0].replace(/Damaged /, '');
		num = parseInt( num.replace(/ hp/, '') );
		damagehp = damagehp - num
		$('#hp-current').text( maxhp - damagehp );
	} else if (hprecord[0].indexOf('Healed') >= 0) {
		var num = hprecord[0].replace(/Healed /, '');
		num = parseInt( num.replace(/ hp/, '') );
		damagehp = damagehp + num;
		$('#hp-current').text( maxhp - damagehp );
	} else if (hprecord[0].indexOf('Added') >= 0) {
		var num = hprecord[0].replace(/Added /, '');
		num = parseInt( num.replace(/ temp hp/, '') );
		temphp = 0;
		$('#hp-temp').text('');
	}
	hprecord.shift();
	displayHPrecord();
})

function displayHPrecord() {
	$('.hprecord-entry').remove();
	if (hprecord.length === 0) {
		$('#hprecord').append( '<li class="hprecord-entry"><i>No entries</i></li>' );
	} else {
		if (hprecord.length < 5) {
			iterations = hprecord.length;
		} else {
			iterations = 5;
		}
		for (i = 0; i < iterations; i++) {
			$('#hprecord').append( '<li class="hprecord-entry">' + hprecord[i] + '</li>' );
		}
	}
}

/* Multiple Spellcasting Display Switch */

$('.spellclass').click(function (e) {
	e.preventDefault();
	var caster = $(this).text().trim();
	console.log( caster );
	$('.spellclass').removeClass('active');
	$('.spellclasstab').addClass('hide');
	$(this).addClass('active');
	$('#spellpage-' + caster ).removeClass('hide');
})

/* Module Card Displays */

$(document).ready(function() {
	$('#spellCard').on('show.bs.modal', function (event) {
		$('#myInput').focus()
		var spell = $(event.relatedTarget) // Button that triggered the modal
		var name = spell.data('spellname');
		var school = spell.data('spellschool');
		if ( spell.data('subschool') ) {
			school = school + ', ' + spell.data('subschool');
		}
		if ( spell.data('descriptor') ) {
			school = school + ', ' + spell.data('descriptor');
		}
		var spelllv = spell.data('spelllv');
		var action = spell.data('spellaction');
		var range = spell.data('spellrange');
		var target = spell.data('spelltarget');
		var area = spell.data('spellarea');
		var effect = spell.data('spelleffect');
		var duration = spell.data('spellduration');
		var save = spell.data('spellsave');
		var resist = spell.data('spellresist');
		var dc = spell.data('spelldc');
		var component = spell.data('spellcomponent');
		var description = spell.data('spelldescription');

		var spellTable = [ school, action, range, target, area, effect, duration, save, resist ];
		var spellTableLabels = ['School', 'Action', 'Range', 'Target',
								'Area', 'Effect', 'Duration', 'Save', 'Resist' ];

		var modal = $(this);
		$('#spellTable').empty();
		modal.find('#spellName').text(name + ' (DC ' + dc + ')');
		modal.find('#spellDescription').html(description);
		modal.find('#spellLv').html('<strong>Level</strong> ' + spelllv);
		modal.find('#spellComponents').html('<strong>Components</strong> ' + component);
		for (i = 0; i < spellTable.length; i++) {
			if (spellTable[i]) {
				$('#spellTable').append(
					'<tr><td class="spell-table-label">' + spellTableLabels[i] +
						'</td><td class="spell-table-entry">' + spellTable[i] + '</td></tr>');
			}
		}
	})

	$('#gearCard').on('show.bs.modal', function (event) {
		$('#myInput').focus();
		var item = $(event.relatedTarget); // Button that triggered the modal
		var name = item.data('name');
		var cost = item.data('cost');
		var weight = item.data('weight');
		var description = item.data('description');

		var modal = $(this);
		modal.find('#gearName').text(name);
		modal.find('#gearDescription').html(description);
		if (cost == "") {
			modal.find('#gearCost').text('-');
		} else {
			modal.find('#gearCost').text(cost);
		}
		if (weight == "") {
			modal.find('#gearWt').text('-');
		} else {
			modal.find('#gearWt').text(weight);
		}
	})

	$('#weaponCard').on('show.bs.modal', function (event) {
		$('#myInput').focus()
		var item = $(event.relatedTarget) // Button that triggered the modal
		var name = item.data('name');
		var category = item.data('category');
		var type = item.data('type');
		var crit = item.data('crit');
		var damage = item.data('damage');
		var quantity = item.data('quantity');
		var weight = item.data('weight');
		var cost = item.data('cost');
		var description = item.data('description');
        var range = item.data('range');

		var modal = $(this);
		modal.find('#weaponName').text(name);
		modal.find('#weaponQty').text(quantity);
		modal.find('#weaponDescription').html(description);
		modal.find('#weaponCategory').text(category);
		modal.find('#weaponType').text(type);
		modal.find('#weaponCrit').text(crit);
		modal.find('#weaponDamage').text(damage);
		modal.find('#weaponCost').text(cost);
		modal.find('#weaponWt').text(weight);
        modal.find('#weaponRange').text(range);
	})

	$('#armorCard').on('show.bs.modal', function (event) {
		$('#myInput').focus()
		var item = $(event.relatedTarget) // Button that triggered the modal
		var title = item.data('name');
		var weight = item.data('weight');
		var cost = item.data('cost');
		var description = item.data('description');

		var modal = $(this);
		modal.find('#armorName').text(title);
		modal.find('#armorDescription').html(description);
		if (cost == "") {
			modal.find('#armorCost').text('-');
		} else {
			modal.find('#armorCost').text(cost);
		}
		if (weight == "") {
			modal.find('#armorWt').text('-');
		} else {
			modal.find('#armorWt').text(weight);
		}
	})

	$('#magicitemCard').on('show.bs.modal', function (event) {
		$('#myInput').focus()
		var item = $(event.relatedTarget) // Button that triggered the modal
		var title = item.data('name')
		if ( item.data('slot') ) {
			title = title + ' (' + item.data('slot') + ')';
		}
		var quantity = item.data('quantity');
		var weight = item.data('weight');
		var cost = item.data('cost');
		var description = item.data('description');

		var modal = $(this);
		modal.find('#magicitemName').text(title);
		modal.find('#magicitemQty').text(quantity);
		modal.find('#magicitemDescription').html(description);
		if (cost == "") {
			modal.find('#magicitemCost').text('-');
		} else {
			modal.find('#magicitemCost').text(cost);
		}
		if (weight == "") {
			modal.find('#magicitemWt').text('-');
		} else {
			modal.find('#magicitemWt').text(weight);
		}
	})

	$('#consumableCard').on('show.bs.modal', function (event) {
		$('#myInput').focus()
		var item = $(event.relatedTarget) // Button that triggered the modal
		var name = item.data('name');
		var quantity = item.data('quantity');
		var cost = item.data('cost');
		var description = item.data('description');

		var modal = $(this);
		modal.find('#consumableName').text(name);
		//modal.find('#consumableQty').text(quantity);
		modal.find('#consumableDescription').html(description);
		if (cost == "") {
			modal.find('#consumableCost').text('-');
		} else {
			modal.find('#consumableCost').text(cost);
		}
	})
})

/* Adjustment Menu */

$('.adjNav').click(function (e) {
    e.preventDefault();
    $('.adjNav').removeClass('active');
    $(this).addClass('active');
    $('.adjustlink').addClass('hide');
    $('.adjustlink.active').removeClass('active');
    if ( $(this).is('#conditions') ) {
        $('.condition').removeClass('hide');
    } else if ( $(this).is('#combatmodifiers') ) {
        $('.combat-modifier').removeClass('hide');
    } else if ( $(this).is('#adjustments') ) {
        $('.adjustment').removeClass('hide');
    }
    $('.adjustlink:visible:first').addClass('active');
    var description = $('.adjustlink:visible:first').find('a').attr('title');
    $('#adj-description').html( description );
});

$('.minion-nav').click(function (e) {
    e.preventDefault();
    $('.minion-nav').removeClass('active');
    $(this).addClass('active');
    $('.minion-content').addClass('hide');
    $('.minion-content').removeClass('active');
    if ($(this).text() == "Overview") {
        $('#minion-overview').removeClass('hide');
    } else if ($(this).text() == "Equipment") {
        $('#minion-equipment').removeClass('hide');
    } else if ($(this).text() == "Spells") {
        $('#minion-spells').removeClass('hide');
    }
});

$('.adjustlink').click(function (e) {
	e.preventDefault();
	var description = $(this).find('a').attr('title');
	$('.adjustlink').removeClass('active');
	$(this).addClass('active');
	$('#adj-description').html( description );
})

/* Summary Module */

var activeAdjustmentList = $('#active-adjustments').html();
var activeAbiList = $('#active-abilities').html();
$('#clone-adjustments').html( activeAdjustmentList );
$('#clone-activeabi').html( activeAbiList );
$('#summary').find( 'input' ).prop('disabled', true);

$('#active-adjustments').on('change', function() {
	activeAdjustmentList = $('#active-adjustments').html();
	$('#clone-adjustments').html( activeAdjustmentList );
	$('#summary').find( 'input' ).prop('disabled', true);
});

$('#active-abilities').on('change', function() {
	activeAbiList = $('#active-abilities').html();
	$('#clone-activeabi').html( activeAbiList );
	$('#summary').find( 'input' ).prop('disabled', true);
});

/* Global Variables */

// Ability Scores
var adjStr = 0;
var adjDex = 0;
var adjCon = 0;
var adjInt = 0;
var adjWis = 0;
var adjCha = 0;
// Ability Checks
var adjAbiCheck = 0;
var adjStrCheck = 0;
var adjDexCheck = 0;
var adjConCheck = 0;
var adjIntCheck = 0;
var adjWisCheck = 0;
var adjChaCheck = 0;
// Attacks
var adjAttack = 0;
var adjMelee = 0;
var adjRanged = 0;
var adjCMB = 0;
// Defenses
var adjDef = 0;
var adjAC = 0;
var adjCMD = 0;
// Saves
var adjSaves = 0;
var adjFort = 0;
var adjRef = 0;
var adjWill = 0;
// Skills
var adjAllSkills = 0;
var adjStrSkills = 0;
var adjDexSkills = 0;
var adjConSkills = 0;
var adjIntSkills = 0;
var adjWisSkills = 0;
var adjChaSkills = 0;
var adjCraft = 0;
var adjKnowledge = 0;
var adjPerform = 0;
// Miscellaneous
var adjInit = 0;
var adjSpeed = 0;
// Hit Points
var hprecord = [];
var damagehp = 0;
var temphp = 0;
var nonlethaldamage = 0;
