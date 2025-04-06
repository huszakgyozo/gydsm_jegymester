import re
from app.blueprints.userrole import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.userrole.schemas import *
from app.blueprints.userrole.service import UserroleService
from jegymester.app.blueprints.userrole.schemas import UserroleListSchema, UserroleRequestSchema, UserroleResponseSchema, UserroleUpdateSchema

# ma

@bp.route('/')
def index():
    return 'Userrole Blueprint'

@bp.get('/list_all')
@bp.output(UserroleListSchema(many=True))
def userrole_list_all():
    success, response = UserroleService.userrole_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.get('/get/<int:id>')
@bp.output(UserroleResponseSchema)
def userrole_get_item(id):
    success, response = UserroleService.userrole_get_item(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.post('/add/')
@bp.input(UserroleRequestSchema, location="json")
@bp.output(UserroleResponseSchema)
def userrole_add_new(json_data):
    success, response = UserroleService.userrole_add(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put('/update/<int:id>')
@bp.input(UserroleUpdateSchema, location="json")
@bp.output(UserroleResponseSchema)
def userrole_update(id, json_data):
    success, response = UserroleService.userrole_update(id, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.delete('/delete/<int:id>')
def userrole_delete(id):
    success, response = UserroleService.userrole_delete(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
