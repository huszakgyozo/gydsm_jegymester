from sqlalchemy.sql.functions import current_user
from config import Config
from app.extensions import db
from apiflask import APIFlask
from config import Config
from app.extensions import db
from app.models import *


from flask import render_template
from flask import Flask, flash, jsonify, redirect, url_for
from app.forms.loginForm import LoginForm
from app.forms.registrationForm import RegistrationForm
from app.forms.movieAddFilm import MovieAddFilm
import requests
from app.extensions import auth
from app.blueprints import role_required, verify_token

#from datetime import timedelta
def create_app(config_class=Config):
    #app = Flask(__name__)

    # API-k kiprobalasahoz
    app = APIFlask(__name__, json_errors=True,
                   title="Jegymester API",
                   docs_path="/swagger")

    

    #app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=1)

    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('index.html', page="index")    

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        
        if form.validate_on_submit():
            

            email = form.email.data
            password = form.password.data
            
            response = requests.post('http://localhost:8888/api/user/login', json={
                'email': email,
                'password_hash': password
            })
            print(response.json())
            if "token" and "email" in response.json():
                
                return render_template('index.html', page="index",data=response.json(),remember=form.remember_me.data)

            else:
                flash("Hibás email cím vagy jelszó!")
                return render_template('login.html', page="login",form=form)
        return render_template('login.html', page="login",form=form)

    @app.route('/registrate',methods=['GET', 'POST'])
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
            print(response.json())
            if "email" in response.json():
                flash('Sikeres regisztráció')
                

            else:
                flash("Nem létezik az e-mail cím vagy már használatban van!")
                return render_template('registrate.html', page="registrate",form=form)
        return render_template('registrate.html', page="registrate", form=form)

    @app.route('/showfilm')
    def showfilm():
        form = MovieAddFilm()

        if form.validate_on_submit():

            title = form.title.data
            duration = form.duration.data
            genre = form.genre.data
            age_limit = form.age_limit.data
            description = form.description.data

            response = requests.post('http://localhost:8888/api/movie/add', json={

                        'title' : title,
                        'duration': duration,
                        'genre': genre,
                        'age_limit': age_limit,
                        'description': description
                })
            if "title" in response.json():
                flash('Sikeres film hozzáadása')

            else:
                flash("Nem sikerült a film hozzáadása!")
                return render_template('movieAdd.html', page="showfilm", form=form)
                
              
        return render_template('movieAdd.html', page="showfilm", form=form)
        
  
    @app.route('/showticket')
    def showticket():
        return render_template('showticket.html', page="showticket")
    


    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    from flask_migrate import Migrate
    migrate = Migrate(app, db, render_as_batch=True)

    # Register blueprints here
    from app.blueprints import bp as bp_default
    app.register_blueprint(bp_default, url_prefix='/api')

    return app