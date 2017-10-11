import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TESTING = False

DATABASE_URI = 'sqlite:////tmp/car_club.db'
SECRET_KEY = '\xb7\x06\xca\xbe\x8f\xda\xf9\x95A\tY+\x1as\xa7\xc7\x11;\xa9i\xc48\xb5o'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'todo.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
