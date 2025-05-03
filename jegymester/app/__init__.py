from email import header
import token
from sqlalchemy.sql.functions import current_user
from config import Config
from app.extensions import db
from apiflask import APIFlask
from config import Config
from app.extensions import db
from app.models import *


from flask import make_response, render_template, request
from flask import Flask, flash, jsonify, redirect, url_for
from app.forms.loginForm import LoginForm
from app.forms.registrationForm import RegistrationForm
from app.forms.movieAddFilm import MovieAddFilm
from app.forms.ticketpurchase import TicketPurchaseForm
import requests
from app.extensions import auth
from app.blueprints import role_required, verify_token, get_auth_headers
from datetime import datetime, timedelta

# from datetime import timedelta


def create_app(config_class=Config):
    # app = Flask(__name__)

    # API-k kiprobalasahoz
    app = APIFlask(__name__, json_errors=True,
                   title="Jegymester API",
                   docs_path="/swagger")

    @app.route('/')
    @app.route('/home')
    def home():
        token = request.cookies.get('token')
        data = verify_token(token)
        if data:
            roles = data["roles"]
            rolesid = set(role['id'] for role in roles)
            return render_template('index.html', page="index", data=data, roles=rolesid)

        return render_template('index.html', page="index")

    @app.route('/logout')
    def logout():
        resp = make_response(redirect(url_for('login')))
        resp.set_cookie('token', '', expires=0)
        flash("Sikeresen kijelentkeztél.")
        return resp

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        token = request.cookies.get('token')
        data = verify_token(token)

        if data:
            return redirect(url_for('home'))

        form = LoginForm()

        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            response = requests.post('http://localhost:8888/api/user/login', json={
                'email': email,
                'password_hash': password
            })
            if verify_token(response.json()["token"]):
                resp = make_response(redirect(url_for('home')))
                resp.set_cookie('token', response.json()["token"])
                return resp
            else:
                flash("Hibás email cím vagy jelszó!")
                return render_template('login.html', page="login", form=form)
        return render_template('login.html', page="login", form=form)

    @app.route('/registrate', methods=['GET', 'POST'])
    def registrate():
        form = RegistrationForm()
        if form.validate_on_submit():
            phone = form.phone.data
            email = form.email.data
            password = form.password.data

            response = requests.post('http://localhost:8888/api/user/registrate', json={
                'phone': phone,
                'email': email,
                'password_hash': password
            })

            if "email" in response.json():
                print(response.json())
                flash('Sikeres regisztráció')
            else:
                flash("Már regisztrált az adott email címmel!")
                return render_template('registrate.html', page="registrate", form=form)
        return render_template('registrate.html', page="registrate", form=form)

    @app.route('/movieadd', methods=['GET', 'POST'])
    def movieadd():

        token = request.cookies.get('token')
        data = verify_token(token)
        if data:
            return redirect(url_for('home'))
        form = MovieAddFilm()

        if form.validate_on_submit():

            title = form.title.data
            duration = form.duration.data
            genre = form.genre.data
            age_limit = form.age_limit.data
            description = form.description.data

            response = requests.post('http://localhost:8888/api/movie/add', json={
                'title': title,
                'duration': duration,
                'genre': genre,
                'age_limit': age_limit,
                'description': description
            }, headers=get_auth_headers(token))

            if "title" in response.json():
                flash('Sikeres film hozzáadása')

            else:
                flash("Nem sikerült a film hozzáadása!")
                return render_template('movieAdd.html', page="movieadd", form=form, data=data)

        return render_template('movieAdd.html', page="showfilm", form=form, data=data)

    @app.route('/movielist')
    def movielist():
        token = request.cookies.get('token')
        data = verify_token(token)
        response = requests.get(
            'http://localhost:8888/api/movie/list_all', headers=get_auth_headers(token))
        movies = response.json()
        return render_template('movielist.html', page="movielist", movies=movies, data=data)


    @app.route('/ticketlist')
    def ticketlist():
        token = request.cookies.get('token')
        data = verify_token(token)

        
        response = requests.get(
            f'http://localhost:8888/api/ticket/get/usertickets/{data["id"]}', headers=get_auth_headers(token))
        ticket = response.json()
        return render_template('showticket.html', page="showticket", tickets=ticket, data=data)

    # Írd meg a ticketpurchase.py alapján az app.route('/ticketpurchase') útvonalat, ahol a felhasználó kiválaszthatja a filmet és a vetítési időpontot. A kiválasztott filmhez tartozó időpontok és helyszínek automatikusan töltődjenek be. Kötelező legyen megadni emailt és telefonszámot! A vásárlás gomb megnyomásakor egy új ablakban jelenjen meg a kiválasztott jegy adatai:
    @app.route('/ticketpurchase', methods=['GET', 'POST'])
    def ticketpurchase():
        token = request.cookies.get('token')
        data = verify_token(token)
        form = TicketPurchaseForm()
        response = requests.get(
            'http://localhost:8888/api/movie/list_all', headers=get_auth_headers(token))
        movies = response.json()
        




    @app.route('/ticket_delete/<int:ticketid>', methods=['GET', 'DELETE'])
    def ticket_delete(ticketid):
        token = request.cookies.get('token')
        data = verify_token(token)
        if data:
            return redirect(url_for('home'))
        response = requests.get(f'http://localhost:8888/api/ticket/get/{ticketid}', headers=get_auth_headers(token))
        ticket = response.json()
        start_time = datetime.strptime(ticket["screening"]["start_time"], "%Y-%m-%d %H:%M:%S")
        if datetime.now() < start_time - timedelta(hours=4):
            response = requests.delete(
                 f'http://localhost:8888/api/ticketorder/delete/{ticketid}', headers=get_auth_headers(token))
            flash("Jegy törlése sikeres.")
        else:
            flash("4 órával a kezdés elött törölhető csak.")
        return ticketlist()




    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    from flask_migrate import Migrate
    migrate = Migrate(app, db, render_as_batch=True)

    # Register blueprints here
    from app.blueprints import bp as bp_default
    app.register_blueprint(bp_default, url_prefix='/api')

    return app