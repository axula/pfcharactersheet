/* Admin Pages */

$('#new').on('shown.bs.modal', function () {
  $('#myInput').focus()
})

function setNavbarActive() {
	var page_name = document.getElementById("page").className;
	document.getElementById("link-" + page_name).className = "active";
}

/* Character Sheet */

$(document).ready(function () {
    $("td").tooltip({container:'body'});
});

$(document).ready(function () {
    $("dd").tooltip({container:'body'});
});

$(document).ready(function () {
    $("span").tooltip({container:'body'});
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

$('#spellCard').on('shown.bs.modal', function () {
  $('#myInput').focus()
})

$('#gearCard').on('shown.bs.modal', function () {
  $('#myInput').focus()
})

$('#adjustmentMenu').on('show.bs.modal', function () {
	$('#adjustmentMenuBody').css('height',$( window ).height()*0.9);
	$('.adj-list').css('height',$( window ).height()*0.9-170);
	$('#adj-description').css('height',$( window ).height()*0.9-170);
});

$('#page-nav a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})

/* Daily Reset Functions */

$('#restedHP').click(function (e) {
	e.preventDefault()
	healnum = parseInt( $(this).attr('title') );
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
})

$('#restedAbilities').click(function (e) {
	e.preventDefault()
	resetTracked();
})

$('#restedSpells').click(function (e) {
	e.preventDefault()
	resetSpells();
})

function resetHP() {
	var maxhp = +($('#hp-max').text())
	damagehp = 0;
	temphp = 0;
	nonlethaldamage = 0;
	$('#hp-current').text( maxhp );
	$('#hp-temp').text('');
	$('#hp-nonlethal').text('');
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
	num = $('#hp-input').val()
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
	damagehp = damagehp + num;
	var hp = $('#hp-current').text();
	hprecord.unshift( 'Damaged ' + num + ' hp' );
	$('#hp-current').text( maxhp - damagehp );
	$('#hp-input').val('');
	displayHPrecord();
})

$('#hp-heal').click(function (e) {
	e.preventDefault()
	var num = +($('#hp-input').val());
	var maxhp = +($('#hp-max').text());
	if (num > damagehp) {
		hprecord.unshift( 'Healed ' + damagehp + ' hp' );
		damagehp = 0;
	} else {
		hprecord.unshift( 'Healed ' + num + ' hp' );
		damagehp = damagehp - num;
	}
	$('#hp-current').text( maxhp - damagehp );
	$('#hp-input').val('');
	displayHPrecord();
})

$('#hp-addtemp').click(function (e) {
	e.preventDefault()
	var num = $('#hp-input').val();
	var hp = $('#hp-current').text();
	hprecord.unshift( 'Added ' + num + ' temp hp' );
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

/* Spell Card Display */

$(document).ready(function() {
	$('#spellCard').on('show.bs.modal', function (event) {
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
		var item = $(event.relatedTarget) // Button that triggered the modal
		var name = item.data('name');
		var cost = item.data('cost');
		var weight = item.data('weight');
		var description = item.data('description');
		
		var modal = $(this);
		modal.find('#gearName').text(name);
		modal.find('#gearDescription').html(description);
		modal.find('#gearCost').text(cost);
		if (weight == "") {
			modal.find('#gearWt').text('-');
		} else {
			modal.find('#gearWt').text(weight);
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
})

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
var adjSkills = 0;
// Miscellaneous
var adjInit = 0;
var adjSpeed = 0;
// Hit Points
var hprecord = [];
var damagehp = 0;
var temphp = 0;
var nonlethaldamage = 0;