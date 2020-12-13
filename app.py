from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
# csrf = CSRFProtect(app)
# csrf.init_app(app)

from config import *


db = SQLAlchemy(app)


db = SQLAlchemy(app, session_options={
    'expire_on_commit': False
})

def db_init(app):
  db.init_app(app)
  
  
  with app.app_context():
    db.create_all()

db_init(app)

from routes import *
from models import Image