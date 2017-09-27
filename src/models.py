from datetime import datetime

from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from src import db


class User(db.Model, UserMixin):
    """User database table"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    cars = db.relationship('Task', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String)

    @property
    def password(self):
        """Raise when attempt to read password"""
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password: str):
        """Generate hash using password as seed"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Validate if password is correct"""
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_name(name: str) -> object:
        """Return owner instance"""
        return User.query.filter_by(name=name).first()

    def __repr__(self) -> str:
        return '<User %r>' % self.username


class Task(db.Model):
    """Task database tables"""
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_due = db.Column(db.DateTime)
    status = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @staticmethod
    def newest(num: int) -> list:
        """Return <num> of latest cars"""
        return Task.query.order_by(desc(Task.date_created)).limit(num)

    @staticmethod
    def get_tasks_for_user(username: User):
        """Return tasks for a particular user"""
        return Task.query.filter_by(user_id=username)

    def __repr__(self) -> str:
        return "<Task '{}': '{}'>".format(self.description, self.date_created)
