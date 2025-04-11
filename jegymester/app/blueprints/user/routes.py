import re
from app.blueprints.user import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.user.schemas import *
from app.blueprints.user.service import UserService
from jegymester.app.blueprints.user.schemas import UserLoginSchema, UserRequestSchema, UserResponseSchema
from jegymester.app.blueprints.user.service import UserService
from app.extensions import auth
from app.blueprints import role_required

# ma


@bp.route('/')
def index():
    return 'User Blueprint'


@bp.post('/registrate')
@bp.input(UserRequestSchema, location="json")
@bp.output(UserResponseSchema)
def user_registrate(json_data):
    sucess, response = UserService.user_registrate(json_data)
    if sucess:
        return response, 200
    raise HTTPError(400, message=response)


@bp.post('/login')
@bp.doc(tags=["user"])
@bp.input(UserLoginSchema, location="json")
@bp.output(UserResponseSchema)
def user_login(json_data):
    success, response = UserService.user_login(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.get('/list_all')
@bp.output(UserListSchema(many=True))
@bp.auth_required(auth)
#meg kell valósítani jelenleg role ID-val működik
#1 admin
#2 user
#3 cashier
@role_required([1])
#@role_required(["Admin"])
def user_list_all():
    success, response = UserService.user_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)