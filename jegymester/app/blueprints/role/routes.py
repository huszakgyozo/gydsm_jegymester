from app.blueprints.role import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.role.schemas import *
from app.blueprints.role.service import RoleService
from jegymester.app.blueprints.role.schemas import RoleResponseSchema, RoleUpdateSchema

# ma

@bp.route('/')
def index():
    return 'Role Blueprint'


@bp.get('/list_all')
@bp.output(RoleListSchema(many=True))
def role_list_all():
    success, response = RoleService.role_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/get/<int:id>')
@bp.output(RoleResponseSchema)
def role_get_item(id):
    success, response = RoleService.role_get_item(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put('/update/<int:id>')
@bp.input(RoleUpdateSchema, location="json")
@bp.output(RoleResponseSchema)
def role_update(id, json_data):
    success, response = RoleService.role_update(id, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.delete('/delete/<int:id>')
def role_delete(id):
    success, response = RoleService.role_delete(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

