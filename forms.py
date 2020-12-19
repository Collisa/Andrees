from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, StringField, SelectField, FileField, TextAreaField, validators
from wtforms.validators import Regexp, InputRequired

from models import Theme

all_themes = Theme.query.all()

class UploadForm(FlaskForm):
  image = FileField('', validators=[Regexp('^\\[^/\\]\.jpg$')]) # regexp doesn't work, everything is okay 
  description = TextAreaField('Omschrijving')
  theme = SelectField('Thema', choices=[theme.theme_name for theme in all_themes])
  position = RadioField('Position', choices=['Thema: Cover', 'Thema: kleine foto', 'Geen geschikt formaat'])
  submit = SubmitField('Upload')
    
  
class NewThemeForm(FlaskForm):
  theme_name = StringField('Naam', validators=[InputRequired()])
  permalink = StringField('Permalink', validators=[Regexp('^[-a-z]*$', message='Ben je zeker dat je enkel kleine letters en koppeltekens hebt gebruikt?')])
  submit = SubmitField('Voeg toe')