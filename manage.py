from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, prompt_bool

from src import app, db
from src.models import Task, User
from helpers.db_init_helpers import USERS, TASKS

manager = Manager(app)


def create_users(conn: SQLAlchemy, users: list):
    for user_args in users:
        conn.session.add(User(**user_args))


def create_tasks(conn: SQLAlchemy, tasks: list):
    for task_args in tasks:
        conn.session.add(Task(**task_args))


def fill_db(conn: SQLAlchemy):
    """Fill database with initial fake data"""
    create_users(conn, USERS)
    create_tasks(conn, TASKS)
    conn.session.commit()


@manager.command
def init_db():
    """Initialize database"""
    db.create_all()
    fill_db(conn=db)
    print('Database has been initialized')


@manager.command
def drop_db():
    """Drop database"""
    msg = 'Are you sure you want to delete your database?'
    if prompt_bool(msg):
        db.drop_all()
        print('Database has been dropped.')


if __name__ == '__main__':
    manager.run()
