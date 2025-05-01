from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField 
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class MovieAddFilm(FlaskForm):
    title = StringField("Film címe")
                         
    duration = IntegerField("Film hossza")
                           
    genre = StringField("Film műfaja")

    age_limit = IntegerField("Korhatár")

    description = StringField("Film leírása")

    submit = SubmitField("Film hozzáadása")

    