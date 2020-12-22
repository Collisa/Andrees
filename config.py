from app import app
from os import environ
import os

basedir = os.path.abspath(os.path.dirname(__file__))


app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOADED_PHOTOS_DEST'] = environ.get('UPLOADED_PHOTOS_DEST')

app.config['RESIZE_URL'] = environ.get('RESIZE_URL')
app.config['RESIZE_ROOT'] = environ.get('RESIZE_ROOT')
app.config['RESIZE_STORAGE_BACKEND'] = environ.get('RESIZE_STORAGE_BACKEND')
app.config['RESIZE_S3_BUCKET'] = environ.get('AWS_BUCKET')
app.config['RESIZE_S3_ACCESS_KEY'] = environ.get('AWS_ACCESS_KEY')
app.config['RESIZE_S3_SECRET_KEY'] = environ.get('AWS_SECRET_KEY')
app.config['RESIZE_S3_REGION'] = environ.get('AWS_REGION')

