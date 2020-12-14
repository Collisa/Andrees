from flask.helpers import url_for
from app import app, db, resize
from flask import render_template, request
from werkzeug.utils import redirect, secure_filename

from forms import UploadForm
from models import Image

import os




all_img = Image.query.all()


@app.route('/')
def home():
  return render_template('home.html', all_img=all_img, app=app, os=os)



@app.route('/thema')
def thema():
  small_img_all = Image.query.filter(Image.position == 'Thema: kleine foto')
  covers = Image.query.filter(Image.position == 'Thema: Cover')
  
  cover = {}
  
  for foto in covers:
    if not foto.theme in covers:
      cover[foto.theme] = []
    cover[foto.theme].append(foto.filename)
  
  thumbnails = {}
  
  for foto in small_img_all:
    if not foto.theme in thumbnails:
      thumbnails[foto.theme] = []
    thumbnails[foto.theme].append(foto.filename)
  
  return render_template('thema.html', thumbnails=thumbnails, os=os, app=app, covers=cover)



@app.route('/upload')
def upload():
  form = UploadForm()
  
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