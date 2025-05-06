from flask_wtf import FlaskForm
from wtforms import SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired

class ScreeningEdit(FlaskForm):
    screening_select = SelectField("Melyik vetítést szeretnéd módosítani?", choices=[], validators=[DataRequired()])
    theater_select = SelectField("Új helyszín", choices=[], validators=[DataRequired()])
    start_time = DateTimeField("Új időpont",format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField("Vetítés módosítása")