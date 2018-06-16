# pfcharactersheet
A python-based web app for importing and display XML output of Pathfinder characters from Hero Lab

<h2>Setup Flask</h2>

This web app is based on <a href="http://flask.pocoo.org/">Flask</a>, a microframework for Python.

Before you install Flask and the necessary components, it's recommended that you first set up a virtual environment in your project's root directory to work in (see <a href="https://pypi.python.org/pypi/virtualenv">here</a> for more details).

Within your the root directory, install Flask and required extensions:

pip install -r requirements.txt

By default, the application is set to run on localhost. You can change it by editing the host in <b>run.py</b>.

<h2>Create the Database</h2>

Initialize the database easily by running <b>create.py</b>. By default, the script creates an "admin" user with the password "temporary", but you can customize this beforehand by editing <b>create.py</b>.

<h2>A Few Comments</h2>

This app, while usable, is still a work in progress. In its current state, it can be used as a static character sheet, displaying all stats and abilities as they appear in Hero Lab.

Hero Lab's XML export is imperfect - there will be some abilities absent from the sheet. For instance, the statistics for an imp familiar for whatever reason does not include its fly speed. Hero Lab simply does not include it in the XML. Also, prepared cleric domain spells will not appear on the cleric's spell list, unless you manually mark the spells as cleric spells.

<h2>Planned Features</h2>

- Conditions and Combat Modifiers (flanking, blinded, etc)
- Custom defined effects (define how spells and abilities affect your game statistics)
- Tracker for currently in use spells and abilities (keep track of buffs you have cast, on who, and how long they last)
