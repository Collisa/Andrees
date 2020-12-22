from app import app, db
from flask import render_template, request, flash, session, g, url_for, redirect
from werkzeug.utils import secure_filename

from forms import UploadForm, NewThemeForm, EditForm
from models import Image, Theme
from user import users
from os import environ

import os
import tempfile

import boto3

s3 = boto3.client('s3',
  aws_access_key_id=environ.get('AWS_ACCESS_KEY'),
  aws_secret_access_key=environ.get('AWS_SECRET_KEY')
)
BUCKET_NAME=environ.get('AWS_BUCKET')

s3resource = boto3.resource('s3', aws_access_key_id=environ.get('AWS_ACCESS_KEY'), aws_secret_access_key=environ.get('AWS_SECRET_KEY'))


@app.route('/')
def home():
  all_img = Image.query.order_by(Image.id.desc())
  return render_template('home.html', all_img=all_img, app=app, os=os)



@app.route('/thema')
def thema():
  small_img_all = Image.query.filter(Image.position == 'Thema: kleine foto').order_by(Image.id.desc())
  covers = Image.query.filter(Image.position == 'Thema: Cover').order_by(Image.id.desc())
  
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
  
  themes_id = []
  themes_permalink = []
  themes_name = []
    
  for theme in Theme.query.all():
    themes_id.append(theme.id)
    themes_permalink.append(theme.permalink)
    themes_name.append(theme.theme_name)
    
  
  return render_template('thema.html', thumbnails=thumbnails, os=os, app=app, covers=cover, themes_id=themes_id, themes_permalink=themes_permalink, themes_name=themes_name)







@app.before_request
def before_request():
  g.user = None
  
  if 'user_id' in session:
    user = [x for x in users if x.id == session['user_id']][0]
    g.user = user


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    session.pop('user_id', None)
    
    username = request.form['username']
    password = request.form['password']
    
    for user in users:
      if user.username == username and user.password == password:
        session['user_id'] = user.id
        return redirect(url_for('upload'))        
    
    return redirect(url_for('login'))
      
  return render_template('login.html')    


@app.route('/logout')
def logout():
  session.pop('user_id', None)
  return redirect(url_for('home'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
  if not g.user:
    return redirect(url_for('login'))
  
  form = UploadForm()
  theme_form = NewThemeForm()
  
  if theme_form.validate_on_submit():   
    new_theme = Theme(
      theme_name=request.form['theme_name'],
      permalink=request.form['permalink'],
    )
    
    if Theme.query.filter(Theme.theme_name == new_theme.theme_name).first() and Theme.query.filter(Theme.permalink == new_theme.permalink).first():
      flash("Ben je zeker dat dit thema nog niet bestaat?")
      
    else:
      db.session.add(new_theme)
      db.session.commit()
      flash("Het thema is toegevoegd!")
      
    
  
  all_img = Image.query.order_by(Image.id.desc())
  return render_template('upload.html', form=form, all_img=all_img, app=app, os=os, theme_form=theme_form)



@app.route('/loading', methods=['POST'])
def uploading():
  if not g.user:
    return redirect(url_for('login'))
  
  file = request.files['image']
  filename = secure_filename(file.filename)
  
  file.save(os.path.join(tempfile.gettempdir(), filename))
  
  s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=os.path.join(tempfile.gettempdir(), filename),
                    Key = 'images/original/' + filename,
                    ExtraArgs={'ACL':'public-read', 'ContentType': 'image/jpeg'}                    
                )
  os.remove(os.path.join(tempfile.gettempdir(), filename))
  
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
  if not g.user:
    return redirect(url_for('login'))
  
  item = Image.query.get(id)
  
  s3resource.Object(BUCKET_NAME, 'images/original/' + item.filename).delete()  
  
  db.session.delete(item)
  db.session.commit()
  
  return redirect(url_for('upload'))


@app.route('/edit/<int:id>')
def edit(id):
  if not g.user:
    return redirect(url_for('login'))
  
  item = Image.query.get(id)
  
  return render_template('edit-form.html', item=item, os=os, app=app, form=EditForm(obj=item))



@app.route('/edit/<int:id>', methods=['POST'])
def update(id):
  if not g.user:
    return redirect(url_for('login'))
  
  item = Image.query.get(id)
  
  form = EditForm()
  
  if form.validate_on_submit():
    item.description=form.description.data
    item.theme=form.theme.data
    item.position=form.position.data
    
    new_theme = Theme.query.filter(Theme.theme_name == form.theme.data).first()
    
    item.theme_id=new_theme.id
    
    db.session.commit()
    return redirect(url_for('upload'))
  
  for error in form.errors:
    for message in form.errors[error]:
      flash(message)
    
  return render_template('edit-form.html', item=item, os=os, app=app, form=EditForm(obj=item))


@app.route('/thema/<int:theme_id>/<permalink>')
def theme_link(theme_id, permalink):
  all_img = Image.query.filter(Image.theme_id == theme_id).order_by(Image.id.desc())
  return render_template('theme_link.html', all_img=all_img, app=app, os=os)