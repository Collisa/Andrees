from app import db

class Image(db.Model):
  
  __tablename__ = 'images'
  
  id = db.Column(db.Integer, primary_key=True)
  filename = db.Column(db.String, unique=True, nullable=False)
  description = db.Column(db.Text)
  theme = db.Column(db.String, nullable=False)
  position = db.Column(db.String)
  

class Theme(db.Model):
  
  __tablename__ = 'themes'
  
  id = db.Column(db.Integer, primary_key=True)
  theme_name = db.Column(db.String, unique=True, nullable=False)
  permalink = db.Column(db.String, unique=True, nullable=False)