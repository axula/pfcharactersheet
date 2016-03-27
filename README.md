# pfcharactersheet
A python-based web app for importing and display XML output of Pathfinder characters from Hero Lab

<h2>Setup Flask</h2>

This web app is based on <a href="http://flask.pocoo.org/">Flask</a>, a microframework for Python. 

Before you install Flask and the necessary components, it's recommended that you first set up a virtual environment in your project's root directory to work in (see <a href="https://pypi.python.org/pypi/virtualenv">here</a> for more details).

Within your the root directory, install Flask and the following extensions: 

$ flask/bin/pip install flask <br>
$ flask/bin/pip install flask-login <br>
$ flask/bin/pip install flask-sqlalchemy <br>
$ flask/bin/pip install sqlalchemy-migrate <br>
$ flask/bin/pip install flask-whooshalchemy <br>
$ flask/bin/pip install flask-wtf

Or if you're on Windows: 

$ flask\Scripts\pip install flask <br>
$ flask\Scripts\pip install flask-login <br>
$ flask\Scripts\pip install flask-sqlalchemy <br>
$ flask\Scripts\pip install sqlalchemy-migrate <br>
$ flask\Scripts\pip install flask-whooshalchemy <br>
$ flask\Scripts\pip install flask-wtf

By default, the application is set to run on localhost. You can change it by editing the host in <b>run.py</b>.

<h2>Create the Database</h2>

Initialize the database easily by running <b>db_create.py</b>. By default, the script creates an "admin" user with the password "temporary", but you can customize this beforehand by editing <b>db_create.py</b>.
