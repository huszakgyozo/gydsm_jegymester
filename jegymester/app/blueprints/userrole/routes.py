import re
from app.blueprints.userrole import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.userrole.schemas import *
from app.blueprints.userrole.service import UserroleService
from app.blueprints.userrole.schemas import UserroleListSchema, UserroleRequestSchema, UserroleResponseSchema, UserroleUpdateSchema
from app.extensions import auth
from app.routes.auth import role_required


# ma

@bp.route('/')
def index():
    return 'Userrole Blueprint'


@bp.get('/list_all')
@bp.output(UserroleListSchema(many=True))
@bp.auth_required(auth)
@role_required([1])
def userrole_list_all():
    success, response = UserroleService.userrole_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.get('/get/<int:id>')
@bp.output(UserroleResponseSchema)
@bp.auth_required(auth)
@role_required([1])
def userrole_get_item(id):
    success, response = UserroleService.userrole_get_item(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.post('/add/')
@bp.input(UserroleRequestSchema, location="json")
@bp.output(UserroleResponseSchema)
@bp.auth_required(auth)
@role_required([1])
def userrole_add_new(json_data):
    success, response = UserroleService.userrole_add(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put('/update/<int:olduserid><int:oldroleid>')
@bp.input(UserroleUpdateSchema, location="json")
@bp.output(UserroleResponseSchema)
@bp.auth_required(auth)
@role_required([1])
def userrole_update(olduserid, oldroleid, json_data):
    success, response = UserroleService.userrole_update(
        olduserid, oldroleid, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.delete('/delete/<int:userid><int:roleid>')
@bp.auth_required(auth)
@role_required([1])
def userrole_delete(userid, roleid):
    success, response = UserroleService.userrole_delete(userid, roleid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
