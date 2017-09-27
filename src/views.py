import time
from random import randint
from datetime import datetime

from flask import render_template, jsonify, redirect, \
    url_for, flash, request
from flask_login import login_required, login_user,\
    logout_user, current_user

from src import app, db, login_manager
from src.forms import TaskForm, LoginForm, SignInForm
from src.models import User, Task


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@app.route('/index')
def index():
    """Index view"""
    return render_template('index.html', new_tasks=Task.newest(5))


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = SignInForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            password=form.password.data,
            email=form.email.data,
        )
        db.session.add(user)
        db.session.commit()
        flash('Rejestracja zakończyła się pomyślnie!')
        return redirect(url_for('login'))
    return render_template('sign_up.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login view"""
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        user = User.get_by_name(name)
        if user is not None and user.check_password(password):
            should_stay_logged = form.remember_me.data
            login_user(user, should_stay_logged)
            flash('Zalogowano {}.'.format(user.name))
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Niepoprawny użytkownik lub hasło.')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Logout view"""
    logout_user()
    return redirect(url_for('index'))


@app.route('/task', methods=['GET', 'POST'])
@login_required
def add_task():
    """View for adding new car"""
    form = TaskForm()
    if form.validate_on_submit():
        description = form.description.data
        # TODO: add date due
        task = Task(user=current_user, description=description)
        db.session.add(task)
        db.session.commit()
        flash('Zapisano zadanie: {}'.format(description))
        return redirect(url_for('index'))
    return render_template('add_task.html', form=form)


@app.route('/some_json')
def some_json():
    """Json example"""
    json_ = {
        'date': datetime.utcnow(),
        'epoch_time': time.time(),
    }
    return jsonify(json_)
