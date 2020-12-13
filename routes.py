from flask.helpers import url_for
from app import app, db, resize
from flask import render_template, request
from werkzeug.utils import redirect, secure_filename

from forms import UploadForm
from models import Image

import os

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/thema')
def thema():
  return render_template('thema.html')

@app.route('/upload')
def upload():
  form = UploadForm()
  
  all_img = Image.query.all()
  
  return render_template('upload.html', form=form, all_img=all_img, app=app, os=os)


@app.route('/loading', methods=['POST'])
def uploading():
  file = request.files['image']
  filename = secure_filename(file.filename)
  file.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))
  
  new_file = Image(
    filename=filename,
    description=request.form['description'],
    theme=request.form['theme'],
    position=request.form['position']
  )
  
  db.session.add(new_file)
  db.session.commit()
  
  return redirect(url_for('upload'))

@app.route('/delete/<int:id>')
def delete(id):
  item = Image.query.get(id)
  os.remove(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], item.filename))
  db.session.delete(item)
  db.session.commit()
  
  return redirect(url_for('upload'))