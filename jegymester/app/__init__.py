from email import header
from pyexpat.errors import messages
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
from app.forms.profileEditForm import profileEditForm
from app.forms.movieEdit import MovieEdit
from app.forms.newScreening import NewScreeningForm
from app.forms.screeningEditForm import ScreeningEdit
from app.forms.validate_ticket import ValidateTicketForm
import requests
from app.extensions import auth
from app.blueprints import role_required, verify_token, get_auth_headers
from datetime import datetime, timedelta


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
        if not data:
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
        ticket=None
        response = requests.get(
            f'http://localhost:8888/api/ticket/get/usertickets/{data["id"]}', headers=get_auth_headers(token))
        if response.ok:
            ticket = response.json()
        else:
            flash("Nincs jegyed még!")
        return render_template('showticket.html', page="showticket", tickets=ticket, data=data)

    def seats_screen_refresh(form):
        form.seat_selection.choices = []
        response = requests.get(
    'http://localhost:8888/api/movie/list_all', headers=get_auth_headers(token))
        movies = response.json()
        for movie in movies:
            title = movie['title']
            for screening in movie.get('screenings', []):
                start_time = screening['start_time']
                theatname = screening['theater']['theatname']
                screening_id = screening['id']

                for seat in screening['theater']['seats']:
                    if not seat['reserved']:
                        seat_id = seat['id']
                        seat_number = seat['seat_number']

                        label = f"{title} - {start_time} - {theatname} - {seat_number}"
                        value = f"{screening_id}|{seat_id}"

                        form.seat_selection.choices.append((value, label))

    @app.route('/ticketpurchase', methods=['GET', 'POST'])
    def ticketpurchase():
        token = request.cookies.get('token')
        data = verify_token(token)
        form = TicketPurchaseForm()
        userid=0
        if data:
            userid=data['id']
            form.phone_number.data="0000"
            form.email.data=data['email']

        seats_screen_refresh(form)
        category = requests.get(
            'http://localhost:8888/api/ticketcategory/list_all')
        cat = category.json()
        

        form.ticket_category.choices = [
            (str(c['id']), f"{c['catname']} - {c['price']} Ft") for c in cat
        ]

        if form.validate_on_submit():
            screen_seat = (form.seat_selection.data).split("|")
            category_id=form.ticket_category.data
            print("Kiválasztott:", screen_seat, "és a ",category_id)
            message=""
            if not data:
                phone = form.phone_number.data
                email = form.email.data

                response = requests.post('http://localhost:8888/api/user/registrate', json={
                    'phone': phone,
                    'email': email,
                    'password_hash': ""
                })

                message=response.json().get('message', '')
                if len(message) == 2:
                    userid=message[1]
                else:
                    userid=response.json().get('id', '')
                    print(userid)
                
            ticketbuy = requests.post(
            'http://localhost:8888/api/ticket/add/', json={
                "screening_id": screen_seat[0],
                "seat_id": screen_seat[1],
                "ticketcategory_id": category_id,
                "user_id": userid
            })

            flash("Sikeres foglalás",ticketbuy.json())
            seats_screen_refresh(form)
        return render_template('ticketpurchase.html', page="ticketpurchase", data=data,ticket_categories=cat,form=form)




    @app.route('/ticket_delete/<int:ticketid>', methods=['GET', 'DELETE'])
    def ticket_delete(ticketid):
        token = request.cookies.get('token')
        data = verify_token(token)
        if not data:
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

    @app.route('/movie_edit', methods=['GET', 'POST'])
    def movie_edit():
        token = request.cookies.get('token')
        data = verify_token(token)
        if not data:
            return redirect(url_for('home'))
        form = MovieEdit()
        movies = requests.get(
            'http://localhost:8888/api/movie/list_active')
        moviesjson = movies.json()
        form.movie_select.choices = [(str(movie['id']), movie['title']) for movie in moviesjson]


        if form.validate_on_submit():
            if form.submit.data:
                movies = requests.put(
                f'http://localhost:8888/api/movie/update/{form.movie_select.data}',json={
                    "description": form.description.data
                    }, headers=get_auth_headers(token))
                flash("Sikeres módosítás.")
            elif form.delete.data:
                response = requests.delete(
                f'http://localhost:8888/api/movie/delete/{form.movie_select.data}'
                ,headers=get_auth_headers(token))
                flash("Film törölve.")
                form.description.data = moviesjson[0]['description']
        else:
            form.description.data = moviesjson[0]['description']
            
        movies = requests.get(
        'http://localhost:8888/api/movie/list_active')
        moviesjson = movies.json()
        form.movie_select.choices = [(str(movie['id']), movie['title']) for movie in moviesjson]

        return render_template('movieEdit.html', page="movieEdit", data=data,form=form,movies=moviesjson)

    @app.route('/new_screening', methods=['GET', 'POST'])
    def new_screening():
        token = request.cookies.get('token')
        data = verify_token(token)
        if not data:
            return redirect(url_for('home'))

        form = NewScreeningForm()

        movies = requests.get('http://localhost:8888/api/movie/list_active')
        theaters = requests.get('http://localhost:8888/api/theater/list')
    
        form.movie_select.choices = [(str(movie['id']), movie['title']) for movie in movies.json()]
        form.theater_select.choices = [(str(theater['id']), theater['theatname']) for theater in theaters.json()]

        if form.validate_on_submit():
            response = requests.post(
                'http://localhost:8888/api/screening/add',
                json={
                    'movie_id': form.movie_select.data,
                    'theater_id': form.theater_select.data,
                    'start_time': form.start_time.data.strftime('%Y-%m-%d %H:%M:%S')
                }, headers=get_auth_headers(token)
            )

            flash(f"Új vetítés sikeresen hozzáadva.")


        return render_template('screeningAdd.html', form=form,data=data, page="new_screening")


    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        token = request.cookies.get('token')
        data = verify_token(token)
        form = profileEditForm()
        if form.validate_on_submit():
            response = requests.post('http://localhost:8888/api/user/update',
                                   json = { "id": data["id"],
                                   "email" : form.email.data,
                                   "phone" : form.phone.data
                                   },
                                    headers=get_auth_headers(token))
            if response.ok:
                flash('Profil adatok sikeresen módosítva.')
            else:
                flash('Az e-mail cim már létezik!')
            
            return redirect(url_for('profile'))
        return render_template('profile.html', form=form, data = data)

    @app.route('/edit_screening', methods=['GET', 'POST'])
    def edit_screening():
        form = ScreeningEdit()
        token = request.cookies.get('token')
        data = verify_token(token)
        screenings_response = requests.get('http://localhost:8888/api/movie/list_all')
        theaters_response = requests.get('http://localhost:8888/api/theater/list')
    
        screenings_json = screenings_response.json()
        theaters_json = theaters_response.json()

        choices = []
        for movie in screenings_json:
            for screening in movie.get('screenings', []):
                choice_id = f"{movie['id']}|{screening['id']}"
                choice_label = f"{movie['title']} - {screening['start_time']} ({screening['theater']['theatname']})"
                choices.append((choice_id, choice_label))

        form.screening_select.choices = choices

        form.theater_select.choices = [(str(t['id']), t['theatname']) for t in theaters_json]

        if form.validate_on_submit():
            start_time_str = form.start_time.data.strftime("%Y-%m-%d %H:%M:%S")
            movie_id, screening_id = form.screening_select.data.split('|')
            response = requests.put(
                f"http://localhost:8888/api/screening/update/{screening_id}",
                json={
                    "theater_id": form.theater_select.data,
                    "start_time": start_time_str,
                    "deleted": False,
                    "movie_id": movie_id
                },
                headers=get_auth_headers(token)
            )

            if response.status_code == 200:
                flash("Vetítés sikeresen módosítva!", "success")
            else:
                flash("Hiba történt a módosítás során.", "danger")
        
            return redirect(url_for('edit_screening'))

        return render_template('edit_screening.html', form=form,data=data,screenings=screenings_json)


    @app.route('/validate_ticket', methods=['GET', 'POST'])
    def validate_ticket():
        token = request.cookies.get('token')
        data = verify_token(token)
        if not verify_token(token):
            return redirect(url_for('home'))

        form = ValidateTicketForm()
        if form.validate_on_submit():
            ticket_id = form.ticket_id.data
            resp = requests.get(
                f'http://localhost:8888/api/ticket/get/{ticket_id}',
                headers=get_auth_headers(token)
            )
            print("hiba: ",resp.json())
            if resp.ok:
                response = requests.delete(
                 f'http://localhost:8888/api/ticketorder/delete/{ticket_id}', headers=get_auth_headers(token))
                flash(f'Jegy érvényesítve!', 'success')
            else:
                flash('Érvényesítés sikertelen.', 'danger')

            return redirect(url_for('validate_ticket'))

        return render_template('validate_ticket.html', form=form,data=data)

                    
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    from flask_migrate import Migrate
    migrate = Migrate(app, db, render_as_batch=True)

    # Register blueprints here
    from app.blueprints import bp as bp_default
    app.register_blueprint(bp_default, url_prefix='/api')

    return app