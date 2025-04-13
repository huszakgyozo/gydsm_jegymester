from app.blueprints.ticket import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.ticket.schemas import *
from app.blueprints.ticket.service import TicketService
from app.extensions import auth
from app.blueprints import role_required

@bp.route('/')
def index():
    return 'Ticket Blueprint'


@bp.get('/list/')
@bp.output(TicketListSchema(many=True))
def ticket_list_all():
    success, response = TicketService.ticket_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/list_all/')
@bp.output(TicketListSchema(many=True))
@bp.auth_required(auth)
@role_required([1])
def ticket_reserved_list_all():
    success, response = TicketService.ticket_reserved_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.post('/add/')
@bp.input(TicketRequestSchema, location="json")
@bp.output(TicketResponseSchema)
@bp.auth_required(auth)
@role_required([2,3])
def ticket_add_new(json_data):
    success, response = TicketService.ticket_add(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put('/update/<int:id>')
@bp.input(TicketRequestSchema, location="json")
@bp.output(TicketResponseSchema)
@bp.auth_required(auth)
@role_required([1])
def ticket_update(id, json_data):
    success, response = TicketService.ticket_update(id, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/get/<int:id>')
@bp.output(TicketToTicketOrder)
@bp.auth_required(auth)
@role_required([1])
def ticketorder_One_ticket(id):
    success, response = TicketService.get_ticket(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)