from flask import Blueprint,current_app, flash, make_response, redirect, render_template, request, url_for, abort
from flask_httpauth import wraps
import requests
from app.extensions import auth
from app.forms.loginForm import LoginForm
from app.forms.registrationForm import RegistrationForm
from authlib.jose import jwt
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/logout')
def logout():
    resp = make_response(redirect(url_for('auth.login')))
    resp.set_cookie('token', '', expires=0)
    flash("Sikeresen kijelentkeztél.")
    return resp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    token = request.cookies.get('token')
    data = verify_token(token)

    if data:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        response = requests.post('http://localhost:8888/api/user/login', json={
            'email': email,
            'password_hash': password
        })
        if verify_token(response.json()["token"]):
            resp = make_response(redirect(url_for('main.home')))
            resp.set_cookie('token', response.json()["token"])
            return resp
        else:
            flash("Hibás email cím vagy jelszó!")
            return render_template('login.html', page="login", form=form)
    return render_template('login.html', page="login", form=form)

@auth_bp.route('/registrate', methods=['GET', 'POST'])
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

def get_auth_headers(token):
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

@auth.verify_token
def verify_token(token):
    if not token:
        token = request.cookies.get('token')
    if not token:
        return None
    try:
        data = jwt.decode(
            token.encode('ascii'),
            current_app.config['SECRET_KEY'],
        )
        if data["exp"] < int(datetime.now().timestamp()):
            return None
        return data
    except:
        return None

def role_required(roles):
    def wrapper(fn):
        @wraps(fn)  
        def decorated_function(*args, **kwargs):
            user_roles = [item["id"] for item in auth.current_user.get("roles")]
            for role in roles:
                if role in user_roles:
                    return fn(*args, **kwargs)        
            abort(401)
        return decorated_function
    return wrapper