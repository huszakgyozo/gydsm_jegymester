from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired

class ValidateTicketForm(FlaskForm):
    ticket_id = IntegerField(
        'Jegy azonosító',
        validators=[DataRequired()]
    )
    submit = SubmitField('Érvényesítés')