from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField 
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    email = StringField("Email cím", 
                           validators=[
                               DataRequired(
                                    message="Kötelező mező!"),
                           ])
    password = PasswordField("Jelszó", validators=[
                                DataRequired()
                           ])
    remember_me = BooleanField("Emlékezz rám")
    submit = SubmitField("Bejelentkezés")