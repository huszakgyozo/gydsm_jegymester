from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, PasswordField,TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class MovieEdit(FlaskForm):
    movie_select  = SelectField("Válaszd ki a szerkesztendő filmet", choices=[])

    description = TextAreaField("Film leírása")
    delete= SubmitField("Film törlése")
    submit = SubmitField("Film adat módosítása")

    