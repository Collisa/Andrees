from app import app, db
from flask import render_template, request, flash, session, g, url_for, redirect
from werkzeug.utils import secure_filename

from forms import UploadForm, NewThemeForm, EditForm
from models import Image, Theme
from user import users

import os







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
  
  return render_template('thema.html', thumbnails=thumbnails, os=os, app=app, covers=cover)







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
    
    user = [x for x in users if x.username == username][0]
    if user and user.password == password:
      session['user_id'] = user.id
      return  redirect(url_for('upload'))
    
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
      permalink=request.form['permalink']
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
  if not g.user:
    return redirect(url_for('login'))
  
  item = Image.query.get(id)
  os.remove(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], item.filename))
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
    print("hier")
    item.description=form.description.data
    item.theme=form.theme.data
    item.position=form.position.data
    db.session.commit()
    return redirect(url_for('upload'))
  
  for error in form.errors:
    for message in form.errors[error]:
      flash(message)
    
  return render_template('edit-form.html', item=item, os=os, app=app, form=EditForm(obj=item))