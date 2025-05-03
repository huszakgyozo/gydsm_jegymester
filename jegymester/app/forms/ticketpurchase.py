from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, PasswordField 
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class TicketPurchaseForm(FlaskForm):
    seat_selection  = SelectField("Válassz vetítést és széket", choices=[])
    ticket_category= SelectField("Jegy kategória", choices=[])
    email = StringField("Email cím", validators=[DataRequired()])
    phone_number = StringField("Telefonszám", validators=[DataRequired()])

    submit = SubmitField("Vásárlás")

