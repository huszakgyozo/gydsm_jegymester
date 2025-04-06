import re
from app.blueprints.user import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.user.schemas import *
from app.blueprints.user.service import UserService
from jegymester.app.blueprints.user.schemas import UserLoginSchema, UserRequestSchema, UserResponseSchema
from jegymester.app.blueprints.user.service import UserService

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
def user_list_all():
    success, response = UserService.user_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)