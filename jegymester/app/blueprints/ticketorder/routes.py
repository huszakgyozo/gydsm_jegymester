from app.blueprints.ticketorder import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.ticketorder.schemas import *

from app.blueprints.ticketorder.service import TicketOrderService


@bp.route('/')
def index():
    return 'TicketOrder Blueprint'


@bp.get('/list/')
@bp.output(TicketOrderListSchema(many=True))
def ticketorder_list_all():
    success, response = TicketOrderService.ticketorder_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.get('/get/<int:id>')
@bp.output(TicketOrderResponseSchema)
def ticketorder_get_item(id):
    success, response = TicketOrderService.ticketorder_get_item(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.post('/add/')
@bp.input(TicketOrderRequestSchema, location="json")
@bp.output(TicketOrderResponseSchema)
def ticketorder_add_new(json_data):
    success, response = TicketOrderService.ticketorder_add(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put('/update/<int:id>')
@bp.input(TicketOrderRequestSchema, location="json")
@bp.output(TicketOrderResponseSchema)
def ticketorder_update(id, json_data):
    success, response = TicketOrderService.ticketorder_update(id, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

#ha a jegy nem aktív, akkor delete
@bp.delete('/delete/<int:id>')
def ticketorder_delete(id):
    success, response = TicketOrderService.ticketorder_delete(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)



@bp.get('/ticket/<int:id1>/<int:id2>')
@bp.output(TicketOrderToTicket)
def ticketorder_ticket(id1, id2):
    success, response = TicketOrderService.ticketorder_ticket(id1, id2)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)