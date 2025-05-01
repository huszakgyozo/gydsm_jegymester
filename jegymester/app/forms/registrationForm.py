from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class RegistrationForm(FlaskForm):
    phone = StringField("Telefonszam",
                           validators=[
                               DataRequired(
                                   message="Kötelező mező!"),
    Regexp(r'^\+?[0-9\s\-]{7,15}$', message="Érvénytelen telefonszám formátum.")
])
    email = StringField("Email cím", 
                           validators=[
                               DataRequired(
                                    message="Kötelező mező!"),
                           ])
    password = PasswordField("Jelszó", validators=[
                                DataRequired()
                           ])
    
    submit = SubmitField("Regisztráció")