import time
from datetime import datetime

from flask import render_template, jsonify, redirect, \
    url_for, flash, request
from flask_login import login_required, login_user,\
    logout_user, current_user

from src import app, db, login_manager
from src.forms import TaskForm, LoginForm, SignInForm
from src.models import User, Task
from src.ical_adapter import import_ical_to_tasks, export_tasks_to_ical, send_ical_file


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@app.route('/index')
def index():
    """Index view"""
    user = current_user
    if hasattr(user, 'id'):
        return render_template('index.html',
                               new_tasks=Task.get_tasks_for_user(user.id))
    return render_template('index.html',
                           new_tasks=Task.newest(5))


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = SignInForm()
    if form.validate_on_submit():
        user = User(
            name=form.user.data,
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
        username = form.username.data
        password = form.password.data
        user = User.get_by_name(username)
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
    return render_template('add_car.html', form=form)

# @app.route('/import', methods=['GET', 'POST'])
# @login_required
# def import_ical():
#     """View for adding new car"""
#     form = ImportForm()
#     if form.validate_on_submit():
#         file = form.file.data
#         tasks = import_ical_to_model()
#         task_num = len(tasks)
#         for task in tasks:
#             db.session.add(task)
#         db.session.commit()
#         flash('Zaimportowano {} elementów'.format(task_num))
#         return redirect(url_for('index'))
#     # TODO: add template
#     return render_template('add_car.html', form=form)


@app.route('/export', methods=['GET'])
@login_required
def export_ical():
    """View for adding new car"""
    user = current_user
    tasks = list(Task.get_tasks_for_user(user.id))
    ical = export_tasks_to_ical(tasks)
    ical['summary'] = '%s_todos' % user.name
    return send_ical_file(ical)
