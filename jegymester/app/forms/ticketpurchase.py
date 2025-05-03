from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, RadioField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange, Length

class TicketPurchaseForm(FlaskForm):
    # A view-ban töltsd fel:
    # form.film_id.choices = [(f.id, f.title) for f in movies]
    movie_id = SelectField(
        "Film címe",
        coerce=int,
        validators=[DataRequired(message="Válassz egy filmet!")]
    )

    # Ha vetítés alapján is szűrsz:
    # form.screening_id.choices = [(s.id, s.start_time.strftime("%Y-%m-%d %H:%M")) for s in screenings]
    screening_id = SelectField(
        "Vetítés időpontja",
        coerce=int,
        validators=[DataRequired(message="Válassz vetítési időpontot!")]
    )

    seat_number = IntegerField(
        "Szék száma",
        validators=[DataRequired(), NumberRange(min=1, max=40, message="Legalább 1-es székszámot adj meg!")]
    )

    # Jegytípus rádiógombokkal
    ticket_type = RadioField(
        "Jegytípus",
        choices=[
            ('adult',    'Felnőtt'),
            ('student',  'Diák'),
            ('senior',   'Nyugdíjas')
        ],
        default='adult',
        validators=[DataRequired(message="Jelöld be a jegytípust!")]
    )

    # Vevő adatok
    customer_mobile = StringField(
        "Telefonszám",
        validators=[DataRequired(), Length(min=2, max=100)]
    )
    customer_email = StringField(
        "Email cím",
        validators=[DataRequired(), Email()]
    )

    submit = SubmitField("Jegyek vásárlása")