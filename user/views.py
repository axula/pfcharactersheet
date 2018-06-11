from flask import render_template, flash, redirect, url_for, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, models
from app.models import User
from .forms import LoginForm, UserForm

''' User Management '''

@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.before_request
def before_request():
    g.user = current_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user.get_id() is not None:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.get_user(username)
        if user is None or not user.check_password(password):
            flash ('Username or password is invalid', 'error')
            return redirect(url_for('login'))
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)
        flash('Logged in successfully.')
        return redirect(url_for('index'))
    return render_template('user/login.html', title="Login", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/user/settings', methods=['GET', 'POST'])
@login_required
def settings():
    user = g.user
    form = UserForm()

    if form.validate_on_submit():
        user.username = form.username.data
        if form.password.data:
            user.set_password(form.password.data)
        user.email = form.email.data

        if form.avatar.data:
            user.set_avatar(form.avatar.data)

        user.save()

        flash('User successfully created.')
        return redirect(url_for('settings'))

    form.username.data = user.username
    form.email.data = user.email

    return render_template('user/settings.html', title=user.username, user=user, form=form)

@app.route('/<userid>/user/new', methods=['GET', 'POST'])
@login_required
def new_user(userid):
    user = g.user

    if user.role != 1:
        return redirect(url_for('index'))

    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        role = 3

        user = User(username, email, password, role)

        flash('User successfully created.')
        return redirect(url_for('index'))

    return render_template('user/new_user.html', title="Create New User", user=user, form=form)
