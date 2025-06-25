import json
import token
from urllib import response
from flask import Blueprint, make_response, render_template, request
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
from datetime import datetime, timedelta
from app.extensions import auth
from app.routes.auth import role_required, verify_token, get_auth_headers
from app.routes.api_helpers import api_get, api_post

from app.blueprints.movie.service import MovieService
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
def home():
    token = request.cookies.get('token')
    data = verify_token(token)
    if data:
        roles = data["roles"]
        rolesid = set(role['id'] for role in roles)
        return render_template('index.html', page="index", data=data, roles=rolesid)

    return render_template('index.html', page="index")

@main_bp.route('/movieadd', methods=['GET', 'POST'])
@auth.login_required
@role_required([1])
def movieadd():
    token = request.cookies.get('token')
    data = verify_token(token)
    if not data:
        return redirect(url_for('main.home'))
    form = MovieAddFilm()

    if form.validate_on_submit():
        title = form.title.data
        duration = form.duration.data
        genre = form.genre.data
        age_limit = form.age_limit.data
        description = form.description.data

        response = api_post('http://localhost:8888/api/movie/add',token,json={
            'title': title,
            'duration': duration,
            'genre': genre,
            'age_limit': age_limit,
            'description': description})

        if "title" in response.json():
            flash('Sikeres film hozzáadása')

        else:
            flash("Nem sikerült a film hozzáadása!")
            return render_template('movieAdd.html', page="movieadd", form=form, data=data)

    return render_template('movieAdd.html', page="showfilm", form=form, data=data)

@main_bp.route('/movielist')
def movielist():
    token = request.cookies.get('token')
    data = verify_token(token)
    #response = api_get('http://localhost:8888/api/movie/list_all', token)

    success, movies_json = MovieService.movie_list_all()
    movies = movies_json
    return render_template('movielist.html', page="movielist", movies=movies, data=data)


@main_bp.route('/ticketlist')
@auth.login_required
def ticketlist():
    token = request.cookies.get('token')
    data = verify_token(token)
    ticket=[]
    #response = api_get(
    #    f'http://localhost:8888/api/ticket/get/usertickets/{auth.current_user['id']}', token)
    from app.blueprints.ticket.service import TicketService
    success, ticketlist_json = TicketService.get_usertickets(auth.current_user['id']) 
    if success:
        ticket = ticketlist_json
    else:
        flash("Nincs jegyed még!")
    return render_template('showticket.html', page="showticket", tickets=ticket, data=data)

def seats_screen_refresh(form):
    form.seat_selection.choices = []
    response = api_get(
'http://localhost:8888/api/movie/list_all', token)
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

@main_bp.route('/ticketpurchase', methods=['GET', 'POST'])
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
    category = api_get(
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

            response = api_post('http://localhost:8888/api/user/registrate', json={
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
                
        ticketbuy = api_post(
        'http://localhost:8888/api/ticket/add/',token, json={
            "screening_id": screen_seat[0],
            "seat_id": screen_seat[1],
            "ticketcategory_id": category_id,
            "user_id": userid
        })

        flash("Sikeres foglalás",ticketbuy.json())
        seats_screen_refresh(form)
    return render_template('ticketpurchase.html', page="ticketpurchase", data=data,ticket_categories=cat,form=form)




@main_bp.route('/ticket_delete/<int:ticketid>', methods=['GET', 'DELETE'])
@auth.login_required
@role_required([1])
def ticket_delete(ticketid):
    token = request.cookies.get('token')
    data = verify_token(token)
    if not data:
        return redirect(url_for('main.home'))
    response = api_get(f'http://localhost:8888/api/ticket/get/{ticketid}',token)
    ticket = response.json()
    start_time = datetime.strptime(ticket["screening"]["start_time"], "%Y-%m-%d %H:%M:%S")
    if datetime.now() < start_time - timedelta(hours=4):
        response = requests.delete(
                f'http://localhost:8888/api/ticketorder/delete/{ticketid}', headers=get_auth_headers(token))
        flash("Jegy törlése sikeres.")
    else:
        flash("4 órával a kezdés elött törölhető csak.")
    return ticketlist()

@main_bp.route('/movie_edit', methods=['GET', 'POST'])
@auth.login_required
@role_required([1])
def movie_edit():
    token = request.cookies.get('token')
    data = verify_token(token)
    if not data:
        return redirect(url_for('main.home'))
    form = MovieEdit()
    movies = api_get(
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
            
    movies = api_get(
    'http://localhost:8888/api/movie/list_active')
    moviesjson = movies.json()
    form.movie_select.choices = [(str(movie['id']), movie['title']) for movie in moviesjson]

    return render_template('movieEdit.html', page="movieEdit", data=data,form=form,movies=moviesjson)

@main_bp.route('/new_screening', methods=['GET', 'POST'])
@auth.login_required
@role_required([1])
def new_screening():
    token = request.cookies.get('token')
    data = verify_token(token)
    if not data:
        return redirect(url_for('main.home'))

    form = NewScreeningForm()

    movies = api_get('http://localhost:8888/api/movie/list_active')
    theaters = api_get('http://localhost:8888/api/theater/list')
    
    form.movie_select.choices = [(str(movie['id']), movie['title']) for movie in movies.json()]
    form.theater_select.choices = [(str(theater['id']), theater['theatname']) for theater in theaters.json()]

    if form.validate_on_submit():
        response = api_post(
            'http://localhost:8888/api/screening/add',token,
            json={
                'movie_id': form.movie_select.data,
                'theater_id': form.theater_select.data,
                'start_time': form.start_time.data.strftime('%Y-%m-%d %H:%M:%S')
            }
        )

        flash(f"Új vetítés sikeresen hozzáadva.")


    return render_template('screeningAdd.html', form=form,data=data, page="new_screening")


@main_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    token = request.cookies.get('token')
    data = verify_token(token)
    form = profileEditForm()
    if form.validate_on_submit():
        response = api_post('http://localhost:8888/api/user/update',token,
                                json = { "id": data["id"],
                                "email" : form.email.data,
                                "phone" : form.phone.data
                                })
        if response.ok:
            flash('Profil adatok sikeresen módosítva.')
        else:
            flash('Az e-mail cim már létezik!')
            
        return redirect(url_for('main.profile'))
    return render_template('profile.html', form=form, data = data)

@main_bp.route('/edit_screening', methods=['GET', 'POST'])
def edit_screening():
    form = ScreeningEdit()
    token = request.cookies.get('token')
    data = verify_token(token)
    screenings_response = api_get('http://localhost:8888/api/movie/list_all')
    theaters_response = api_get('http://localhost:8888/api/theater/list')
    
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
        # response = requests.put(
        #     f"http://localhost:8888/api/screening/update/{screening_id}",
        #     json={
        #         "theater_id": form.theater_select.data,
        #         "start_time": start_time_str,
        #         "deleted": False,
        #         "movie_id": movie_id
        #     },
        #     headers=get_auth_headers(token)
        # )
        from app.blueprints.screening.service import ScreeningService
        status,response=ScreeningService.screening_update(screening_id,{
                "theater_id": form.theater_select.data,
                "start_time": start_time_str,
                "deleted": False,
                "movie_id": movie_id
            })

        if status:
            flash("Vetítés sikeresen módosítva!", "success")
        else:
            flash("Hiba történt a módosítás során.", "danger")
        
        return redirect(url_for('main.edit_screening'))

    return render_template('edit_screening.html', form=form,data=data,screenings=screenings_json)


@main_bp.route('/validate_ticket', methods=['GET', 'POST'])
def validate_ticket():
    token = request.cookies.get('token')
    data = verify_token(token)
    if not verify_token(token):
        return redirect(url_for('main.home'))

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

        return redirect(url_for('main.validate_ticket'))

    return render_template('validate_ticket.html', form=form,data=data)