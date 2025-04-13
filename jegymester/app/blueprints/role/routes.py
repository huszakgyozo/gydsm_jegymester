from app.blueprints.role import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.role.schemas import *
from app.blueprints.role.service import RoleService
from jegymester.app.blueprints.role.schemas import RoleResponseSchema, RoleUpdateSchema
from app.extensions import auth
from app.blueprints import role_required
# ma

@bp.route('/')
def index():
    return 'Role Blueprint'


@bp.post('/add/')
@bp.input(RoleRequestSchema, location="json")
@bp.auth_required(auth)
@role_required([1])
def role_add(json_data):
    success, response = RoleService.role_add(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)


@bp.get('/list_all')
@bp.output(RoleListSchema(many=True))
@bp.auth_required(auth)
@role_required([1])
def role_list_all():
    success, response = RoleService.role_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.put('/update/<int:id>')
@bp.input(RoleUpdateSchema, location="json")
@bp.output(RoleResponseSchema)
@bp.auth_required(auth)
@role_required([1])
def role_update(id, json_data):
    success, response = RoleService.role_update(id, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.delete('/delete/<int:id>')
@bp.auth_required(auth)
@role_required([1])
def role_delete(id):
    success, response = RoleService.role_delete(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/myroles')
@bp.output(RoleListSchema(many=True))
@bp.auth_required(auth)
def list_user_roles():
    success, response = RoleService.list_user_roles(auth.current_user.get("id"))
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)