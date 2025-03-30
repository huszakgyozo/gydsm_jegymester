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