from flask_wtf import FlaskForm
from wtforms import SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired

class NewScreeningForm(FlaskForm):
    movie_select = SelectField("Válaszd ki a filmet", choices=[], validators=[DataRequired()])
    theater_select = SelectField("Válaszd ki a helyszínt", choices=[], coerce=int, validators=[DataRequired()])
    start_time = DateTimeField("Vetítés időpontja", format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField("Új vetítés hozzáadása")