from app.blueprints.ticketcategory import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.ticketcategory.schemas import *
from app.blueprints.ticketcategory.service import TicketCategoryService
from app.extensions import auth
from app.routes.auth import role_required

@bp.route('/')
def index():
    return 'TicketCategory Blueprint'


@bp.get('/list_all')
@bp.output(TicketCategoryListSchema(many=True))
def ticketcategory_list_all():
    success, response = TicketCategoryService.ticketcategory_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.get('/get/<int:id>')
@bp.output(TicketCategoryResponseSchema)
def ticketcategory_get_item(id):
    success, response = TicketCategoryService.ticketcategory_get_item(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.put('/update/<int:id>')
@bp.auth_required(auth)
@role_required([1])
@bp.input(TicketCategoryRequestSchema, location="json")
@bp.output(TicketCategoryResponseSchema)
def ticketcategory_update(id, json_data):
    success, response = TicketCategoryService.ticketcategory_update(id, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
