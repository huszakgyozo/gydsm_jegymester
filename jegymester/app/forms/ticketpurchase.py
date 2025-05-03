# Írd meg a jegyvásárlás formját a következőképpen: legördülő menüben választható legyen a film és a vetítési időpont. A kiválasztott filmhez tartozó időpontok és helyszínek automatikusan töltődjenek be. Kötelező legyen megadni emailt és telefonszámot! A vásárlás gomb megnyomásakor egy új ablakban jelenjen meg a kiválasztott jegy adatai:

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField 
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class TicketPurchaseForm(FlaskForm):
    movie = StringField("Film cím", validators=[DataRequired()])
    start_time = StringField("Vetítési időpont", validators=[DataRequired()])
    theatname = StringField("Helyszín", validators=[DataRequired()])

    # szék kiválasztás legördülő listából:
    seat_number = StringField("Szék", validators=[DataRequired()])


    email = StringField("Email cím", validators=[
                        DataRequired(), Length(min=6, max=35)])
    phone_number = StringField("Telefonszám", validators=[
                               DataRequired(), Length(min=10, max=15)])

    submit = SubmitField("Vásárlás")

