from app.blueprints.ticketorder import bp
from apiflask.fields import String, Integer
from apiflask import HTTPError

from app.blueprints.ticketorder.schemas import *
from app.blueprints.ticketorder.service import TicketOrderService
from app.extensions import auth
from app.routes.auth import role_required


@bp.route('/')
def index():
    return 'TicketOrder Blueprint'


@bp.get('/list/')
@bp.output(TicketOrderListSchema(many=True))
@bp.auth_required(auth)
@role_required([1])
def ticketorder_list_all():
    success, response = TicketOrderService.ticketorder_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


# ha a jegy nem aktív, akkor delete
@bp.delete('/delete/<int:ticket_id>')
@bp.auth_required(auth)
#@role_required([1])
def ticketorder_delete(ticket_id):
    success, response = TicketOrderService.ticketorder_delete(ticket_id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
