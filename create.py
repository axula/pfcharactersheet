from app import db, models
import os

os.system('python manage.py db init')
os.system('python manage.py db migrate')
os.system('python manage.py db upgrade')

admin = models.User('admin', '', 'temporary', 1)
db.session.add(admin)
db.session.commit()
