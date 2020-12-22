from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, StringField, SelectField, FileField, TextAreaField, validators
from wtforms.validators import Regexp, InputRequired, Required

from models import Theme


class UploadForm(FlaskForm):
  def __init__(self, all_themes):
      super(UploadForm, self).__init__()
      self.theme.choices = [theme.theme_name for theme in all_themes]
      
  image = FileField('', validators=[Regexp('^\\[^/\\]\.jpg$')]) # regexp doesn't work, everything is okay 
  description = TextAreaField('Omschrijving')
  theme = SelectField('Thema', choices=[])
  position = RadioField('Position', choices=['Thema: Cover', 'Thema: kleine foto', 'Geen geschikt formaat'])
  submit = SubmitField('Upload')
    
  
class NewThemeForm(FlaskForm):
  theme_name = StringField('Naam', validators=[InputRequired()])
  permalink = StringField('Permalink', validators=[Regexp('^[-a-z]*$', message='Ben je zeker dat je enkel kleine letters en koppeltekens hebt gebruikt?')])
  submit = SubmitField('Voeg toe')
  
class EditForm(FlaskForm):
  def __init__(self, all_themes, **kwargs):
      super(EditForm, self).__init__(**kwargs)
      self.theme.choices = [theme.theme_name for theme in all_themes]
      
  description = TextAreaField('Omschrijving')
  theme = SelectField('Thema', choices=[])
  position = RadioField('Position', choices=['Thema: Cover', 'Thema: kleine foto', 'Geen geschikt formaat'])
  submit = SubmitField('Wijzig')
     