from email import message
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField 
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class profileEditForm(FlaskForm):
    email = StringField("Email cím", validators=[])                                                 
    phone = StringField("Telefonszám", validators=[Regexp(r'^\+?[0-9\s\-]{7,15}$', message="Érvénytelen telefonszám formátum.")])
    submit = SubmitField("Módosítom")