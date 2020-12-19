from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_resize   
# from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
# csrf = CSRFProtect(app)
# csrf.init_app(app)

from config import *



resize = flask_resize.Resize(app)



db = SQLAlchemy(app)

from routes import *
from models import *

migrate = Migrate(app, db)


db = SQLAlchemy(app, session_options={
    'expire_on_commit': False
})

def db_init(app):
  db.init_app(app)
  
  
  with app.app_context():
    db.create_all()

db_init(app)

