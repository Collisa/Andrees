from wtforms import Form, SubmitField, RadioField, StringField, SelectField, FileField, TextAreaField, validators

class UploadForm(Form):
  image = FileField('', [validators.regexp(u'^\\[^/\\]\.jpg$')])
  description = TextAreaField('Omschrijving')
  theme = SelectField('Thema', choices=['Libellen', 'Dieren', 'Bloemen', 'Vlinders', 'Winter', 'Katten', 'Vogels', 'Natuur', 'Coloured skies'])
  position = RadioField('Position', choices=['Thema: Cover', 'Thema: kleine foto', 'Geen geschikt formaat'])
  submit = SubmitField('Upload')
    