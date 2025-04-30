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
import requests
from app.extensions import auth
from app.blueprints import role_required, verify_token

def create_app(config_class=Config):
    #app = Flask(__name__)

    # API-k kiprobalasahoz
    app = APIFlask(__name__, json_errors=True,
                   title="Jegymester API",
                   docs_path="/swagger")

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
        return render_template('registrate.html', page="registrate")

    @app.route('/showfilm')
    def showfilm():
        return render_template('showfilm.html', page="showfilm")

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