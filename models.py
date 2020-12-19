from app import db

class Image(db.Model):
  
  __tablename__ = 'images'
  
  id = db.Column(db.Integer, primary_key=True)
  filename = db.Column(db.String, unique=True, nullable=False)
  description = db.Column(db.Text)
  theme = db.Column(db.String, nullable=False)
  position = db.Column(db.String)
  theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'), nullable=False)
  

class Theme(db.Model):
  
  __tablename__ = 'themes'
  
  id = db.Column(db.Integer, primary_key=True)
  theme_name = db.Column(db.String, unique=True, nullable=False)
  permalink = db.Column(db.String, unique=True, nullable=False)
  images = db.relationship('Image', backref='themes', lazy=True)